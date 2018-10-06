package lib

import (
	"bytes"
	"fmt"
	"net"
	"strconv"
)

// Use net.Conn.Write for sending small messages (size < 1024 bytes)
// In other cases use this function
func WriteMessage(message []byte, con net.Conn) {
	cycles := strconv.Itoa((len(message) / 1024) + 1)
	r_based := []rune(cycles)
	lnt := len(r_based)
	var buffer bytes.Buffer
	for i := lnt; i < 1024; i++ {
		buffer.WriteString("0")
	}
	for j := 0; j < lnt; j++ {
		buffer.WriteString(string(r_based[j]))
	}
	con.Write([]byte(buffer.String()))
	con.Write(message)
}

// Use net.Conn.Read for reading small messages (size < 1024 bytes)
// In other cases use this function
func ReadMessage(conn net.Conn) []byte {
	var wMsg []byte
	var message = make([]byte, 1024)
	var c int
	l, err := conn.Read(message)
	if err != nil {
		fmt.Println(err)
		conn.Close()
		return []byte("")
	}
	if l > 0 {
		c, _ = strconv.Atoi(string(message))
	} else {
		return []byte("")
	}
	message = make([]byte, 1024)
	for n := c; n > 0; n-- {
		l, err := conn.Read(message)
		if err != nil {
			fmt.Println(err)
			conn.Close()
			return []byte("")
		}
		if l > 0 {
			wMsg = append(wMsg, message...)
			// fmt.Println("Message received: " + string(message))
		} else {
			break
		}
	}
	return wMsg
}
