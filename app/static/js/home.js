document.querySelector(".send").addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        sendMessage()
    }
})


const token = localStorage.getItem("token");
const url = `http://127.0.0.1:5000?token=${token}`;

const socket = io(url);


// Подключение
socket.on("connect", () => {
    console.log("Connected to server");
});

socket.on("connect_error", (err) => {
    console.error("Ошибка подключения:", err);
});

socket.on("receive_message", (data) => {
    active_chat = document.querySelector(".active")?.dataset.id
    console.log(active_chat)
    if (active_chat == data.chat_id && data.user_id !== localStorage.getItem("user_id")) {
        create_message({message: data.text, id: data.message_id}, data.user_id)
    }
});

socket.on("edited_message", (data) => {
    active_chat = document.querySelector(".active")?.dataset.id
    if (active_chat == data.chat_id && data.user_id !== localStorage.getItem("user_id")) {
        document.querySelector(`[data-id="${data.message_id}"]`).querySelector("p").innerText = data.text
    }
});

socket.on("join_chat", (data) => {
    socket.emit("join_chat", {
        "chat_id": data.chat_id,
    })

    if (data.user_id !== localStorage.getItem("user_id")) {
        const list = document.querySelector('.friend-list');
        const li = document.createElement('li');
        li.innerText = data.chat_name;
        li.classList.add('friend');
        li.addEventListener('click', () => {
            document.querySelectorAll('.friend').forEach(f => f.classList.remove('active'));
            li.classList.add('active');

            document.querySelector('.chat-header').querySelector("h3").innerText = data.chat_name;

            getMessege(data.chat_id)
        })
        li.dataset.id = data.chat_id;
        list.prepend(li);
    } else {
        document.querySelector(".active").dataset.new_chat = false
    }
})


fetch('/auth/check_token', {
    method: 'POST',
    credentials: "include",
})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (!data.status) throw Exeption(data.message);
    })
    .catch(error => {
        console.error('Ошибка запроса:', error)
        window.location.href = '/auth/login'
    });

const logout = () => {
    localStorage.removeItem('token')
    window.location.href = '/auth/login'
}

const load_chats = () => {
    fetch("/get_friends", {
        method: 'POST',
        credentials: "include",
    }).then(response => response.json())
        .then(data => {
            document.querySelector('.friend-list').innerHTML = '';
            for (const d of data.chats) {
                if (d[2] === false) {

                }
                showFriend(d[0], d[1])
            }
        })
}

load_chats()

const getMessege = (chat_id) => {
    fetch('/get_message', {
        method: 'POST',
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({chat_id: chat_id})
    }).then(response => response.json())
        .then(data => {
            load_messeges(data.messages)
        })
}

const load_messeges = (messages) => {
    const user_id = localStorage.getItem("user_id")
    const content = document.querySelector('.messages');
    content.innerHTML = '';
    messages.forEach(message => {
        const div = document.createElement('div');
        div.classList.add("message_box")
        div.setAttribute("style", message.sender_id === user_id ? "justify-content: flex-start" : "justify-content: flex-end")
        div.setAttribute("data-id", `${message.message_id}`)

        div.innerHTML = `
            <p class="message ${message.sender_id === user_id ? "sent" : "received"}">${message.content}</p>
            ${
            message.sender_id === user_id ? '<span class="edit-btn" onclick="editMessage(this)">✏</span>' : ""}
        `

        content.appendChild(div);
        scrollToBottom()
    })
}

const sendMessage = () => {
    const messageInput = document.querySelector('#message_input').value.trim();
    let chat_id = Number(document.querySelector('.active').dataset.id);

    if (document.querySelector('.active').dataset.new_chat) {
        chat_id = 0
    }

    if (messageInput === "") return

    fetch('/send_message', {
        method: 'POST',
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "message": messageInput,
            "sender_id": localStorage.getItem("user_id"),
            "chat_id": chat_id
        })
    }).then(response => {
        if (!response.ok) throw new Error(response.status);

        return response.json()
    })
        .then(data => {
            document.querySelector('.chat-footer').querySelector('input').value = '';

            create_message({message: messageInput, id: data.message_id}, localStorage.getItem("user_id"))

            socket.emit("send_message", {
                "text": messageInput,
                "chat_id": data.chat_id,
                "user_id": localStorage.getItem("user_id"),
                "message_id": data.message_id
            })
        })
        .catch(e => {
            if (e.message === "404") {
                fetch("/create_new_chat", {
                    method: 'POST',
                    credentials: "include",
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({"id": Number(document.querySelector('.active').dataset.id)})
                }).then(response => {
                    if (!response.ok) throw new Error(response.status);

                    return response.json()
                })
                    .then(data => {
                        fetch('/send_message', {
                            method: 'POST',
                            credentials: "include",
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                "message": messageInput,
                                "sender_id": localStorage.getItem("user_id"),
                                "chat_id": data.chat_id
                            })
                        }).then(response => {
                            if (!response.ok) throw new Error(response.status);

                            return response.json()
                        })
                            .then(data => {
                                document.querySelector('.chat-footer').querySelector('input').value = '';

                                create_message(messageInput, localStorage.getItem("user_id"))

                                socket.emit("send_message", {
                                    "text": messageInput,
                                    "chat_id": data.chat_id,
                                    "user_id": localStorage.getItem("user_id"),
                                    "message_id": data.message_id
                                })
                            }).catch(e => {
                            console.log("ну реально хз что произошло")
                        })
                    })
            }
        })
}

const create_message = (message, user_id) => {
    const content = document.querySelector('.messages');
    const div = document.createElement('div');

    div.classList.add("message_box")
    div.setAttribute("style", "justify-content: flex-start")

    div.setAttribute("data-id", `${message.id}`)
    div.innerHTML = `
            <p class="message sent">${message.message}</p>
        <span class="edit-btn" onclick="editMessage(this)">✏</span>
        `
    content.appendChild(div);
    scrollToBottom()
}

function scrollToBottom() {
    const messagesContainer = document.querySelector(".messages");
    const lastMessage = messagesContainer.lastElementChild;
    if (lastMessage) {
        lastMessage.scrollIntoView({behavior: "smooth"});
    }
}


const searchFriends = () => {
    const inputValue = document.querySelector(".search-bar").querySelector("input").value.trim()

    if (inputValue !== "") {
        const url = new URL(window.location);
        url.searchParams.set("s", inputValue);
        window.history.pushState({}, "", url);

        friend_list = document.querySelector(".friend-list")

        user_chats = friend_list.querySelectorAll("li")

        friend_list.innerHTML = ""

        is_found_in_list = false

        for (const chat of user_chats) {
            console.log(chat.innerText)
            if (chat.innerText.includes(inputValue)) {
                is_found_in_list = true

                friend_list.appendChild(chat)
            }
        }

        if (is_found_in_list) return

        fetch("/find_friends", {
            method: "POST",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({"username": inputValue})
        }).then(res => {
            return res.json()
        })
            .then(data => {
                document.querySelector('.friend-list').innerHTML = '';
                for (const user of data.users) {
                    const list = document.querySelector('.friend-list');
                    const li = document.createElement('li');
                    li.innerText = user[0];
                    li.classList.add('friend');
                    li.addEventListener('click', () => {
                        document.querySelectorAll('.friend').forEach(f => f.classList.remove('active'));
                        li.classList.add('active');

                        document.querySelector('.chat-header').querySelector("h3").innerText = user[0];

                        document.querySelector('.messages').innerHTML = ''
                    })
                    li.dataset.id = user[1];
                    li.dataset.new_chat = true;
                    list.appendChild(li);
                }
            })
            .catch(e => {
                console.error(e.status);
            })
    } else {
        if (window.location.search) {
            const url = new URL(window.location);
            url.searchParams.delete("s");
            window.history.pushState({}, "", url);

            load_chats()
        }
    }
}

const showFriend = (chat_name, id) => {
    const list = document.querySelector('.friend-list');
    const li = document.createElement('li');
    li.innerText = chat_name;
    li.classList.add('friend');
    li.addEventListener('click', () => {
        document.querySelectorAll('.friend').forEach(f => f.classList.remove('active'));
        li.classList.add('active');

        document.querySelector('.chat-header').querySelector("h3").innerText = chat_name;

        getMessege(id)
    })
    li.dataset.id = id;
    list.appendChild(li);
}

const editMessage = (e) => {
    const id = Number(e.parentElement.dataset.id)
    const message = e.parentElement.querySelector("p").innerText
    const input = document.getElementById("message_input")

    input.value = message

    const button = document.createElement("button")
    button.classList.add("close-btn")
    button.addEventListener("click", closeEdit)
    button.innerText = "X"

    input.parentElement.append(button)

    document.querySelector(".send").setAttribute("onclick", `editMessageRes(${id})`)
}

const editMessageRes = (id) => {
    const message = document.querySelector("#message_input").value.trim()
    if (message === "") return
    console.log(id)

    fetch("/edit_message", {
        method: "POST",
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"content": message, "message_id": id})
    }).then(res => {
        if (!res.ok) throw Error((res.json()).error)

        return res.json()
    }).then(data => {
        closeEdit()
        document.querySelector(`[data-id="${id}"]`).querySelector("p").innerText = message

        socket.emit("edit_message", {
            "text": message,
            "chat_id": data.chat_id,
            "user_id": localStorage.getItem("user_id"),
            "message_id": id
        })
    }).catch(e => {
        console.log(e)
    })
}

const closeEdit = () => {
    document.querySelector("#message_input").value = ""
    document.querySelector(".close-btn").remove()
    document.querySelector(".send").setAttribute("onclick", "sendMessage()")
}