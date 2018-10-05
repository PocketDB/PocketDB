package main

import (
	"fmt"
	"os"
	"strings"
)

func printPrompt() {
	fmt.Print("db > ")
}

func handler(text string) {
	if strings.Compare(text, ".exit") == 0 {
		os.Exit(0)
	} else {
		fmt.Println("Command not found")
	}
}

func inputPrompt() {
	var text string
	fmt.Scanln(&text)
	handler(text)
}

func main() {
	for {
		printPrompt()
		inputPrompt()
	}
}
