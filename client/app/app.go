package app

import (
	"fmt"
	"net"

	"../../lib"
)

type App struct {
}

func (app *App) Start() {
	fmt.Println("Starting client..")
	con, err := net.Dial("tcp", ":8000")
	if err != nil {
		fmt.Println(err)
	}
	message := []byte("Hello from client!")
	lib.WriteMessage(message, con)
	for {
		fmt.Println("Reading from server")
		msg := make([]byte, 1024)
		l, err := con.Read(msg)
		if err != nil {
			fmt.Println(err)
			break
		}
		if l > 0 {
			fmt.Println("Server's response: " + string(msg))
		} else {
			break
		}
	}
}
