package app

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"

	"../../lib"
)

type App struct {
}

func (app *App) Start() {
	var smsg []byte
	var convmsg string
	fmt.Println("Starting client..")
	con, err := net.Dial("tcp", ":8000")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println("Enter command after the PocketDB > prompt. Enter .q to exit")
	for {
		var message []byte
		fmt.Print("PocketDB > ")
		inputReader := bufio.NewReader(os.Stdin)
		input, _ := inputReader.ReadString('\n')
		input = strings.TrimSpace(input)
		if input == ".q" {
			fmt.Println("Exiting..")
			os.Exit(0)
		}
		message = []byte(input)
		lib.WriteMessage(message, con)
		smsg = lib.ReadMessage(con)
		convmsg = string(smsg)
		if convmsg == "" {
			fmt.Printf("Couldn't get response from server\n")
			continue
		}
		fmt.Println("Server's response:", convmsg)
	}
}
