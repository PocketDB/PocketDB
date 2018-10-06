package app

import (
	"fmt"
	"log"
	"net"

	"../../lib"
	"../core"
)

type App struct {
}

func (app *App) StartListening() {
	ln, err := net.Listen("tcp", ":8000")
	fmt.Println("Server started")
	if err != nil {
		log.Fatal(err)
	}
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Printf("startWorker: %v", err)
			continue
		}
		fmt.Println("Connected to a new client")
		go app.handleConnection(conn)
	}
}

func (app *App) handleConnection(conn net.Conn) {
	for {
		var wMsg []byte
		fmt.Print("Reading message from client: ")
		wMsg = lib.ReadMessage(conn)
		if string(wMsg) == "" {
			fmt.Println("\nClient disconnected")
			break
		}
		fmt.Println(string(wMsg))
		p := core.ParseQuery(wMsg)
		fn := p.Fn
		arg := p.Load
		res := fn(arg)
		//fmt.Println("Writing to client: " + string(res))
		lib.WriteMessage(res, conn)
	}
}
