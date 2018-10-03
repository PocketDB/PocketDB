package core

type parseResult struct {
	Fn   func(arg string) []byte
	Load string
}

var fnmap = map[string]func(arg string) []byte{
	"createTable": createTable,
}

func ParseQuery(msg []byte) parseResult {
	// parse the message into function name and the arguments
	p := parseResult{createTable, "hello"}
	return p
}

func createTable(query string) []byte {
	// implementation to create a table
	// return result of the operation
	return []byte("Output of the query")
}
