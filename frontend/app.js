const bodyElement = document.getElementById("wrapper")

const user = Date.now()
const players = document.getElementById("players")
const player = document.createElement("div")
player.id = (user).toString()
player.style.top = 0
player.style.left = 0
players.appendChild(player)

const ws = new WebSocket(`ws://0.0.0.0:8000/ws/${user}`)

bodyElement.addEventListener('keyup', event => {
    let top = player.style.top ? player.style.top : 0
    let left = player.style.left ? player.style.left : 0
    const step = 5

    if (event.code == "ArrowUp") {
        player.style.top = parseInt(top) - step + "px"
    } else if (event.code == "ArrowDown") {
        player.style.top = parseInt(top) + step + "px"
    } else if (event.code == "ArrowLeft") {
        player.style.left = parseInt(left) - step + "px"
    } else if (event.code == "ArrowRight") {
        player.style.left = parseInt(left) + step + "px"
    }

    let position = {
        event: "move",
        user: (user).toString(),
        top: player.style.top,
        left: player.style.left
    }

    ws.send(JSON.stringify(position))
})

ws.onmessage = response => {
    let data = JSON.parse(response.data)
    console.log(data)
    if (data.event == "create") {
        if (document.getElementById(data.user) == null) {
            const newPlayer = document.createElement("div")
            newPlayer.id = (data.user).toString()
            newPlayer.style.top = 0
            newPlayer.style.left = 0
            document.getElementById("players").appendChild(newPlayer)
        }
    } else if (data.event == "move") {
        player = document.getElementById(`${data.user}`)
        player.style.top = data.top
        player.style.left = data.left
    } else if (data.event == "delete") {
        var player = document.getElementById(`${data.user}`);
        player.remove();
    }
}