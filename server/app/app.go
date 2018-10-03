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
	var wMsg []byte
	fmt.Println("Reading message from client")
	wMsg = lib.ReadMessage(conn)
	fmt.Println("Client sent message: " + string(wMsg))
	p := core.ParseQuery(wMsg)
	fn := p.Fn
	arg := p.Load
	res := fn(arg)
	fmt.Println("Writing to client: " + string(res))
	conn.Write(res)
}
