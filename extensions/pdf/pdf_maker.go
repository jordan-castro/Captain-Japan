package main

import (
	"os"
	"strings"

	"github.com/jung-kurt/gofpdf"
)

func main() {
	// Get the files (pages) for the PDF
	filesToAdd := ReadInput()
	outputFile := filesToAdd[len(filesToAdd)-1]
	// Pop off the last item as it is the output file
	filesToAdd = filesToAdd[:len(filesToAdd)-1]

	// Create a new pdf "object"
	pdf := gofpdf.New("P", "mm", "A4", "")
	// Set the font
	pdf.SetFont("Arial", "", 12)

	// Loop through the files
	for i := 0; i < len(filesToAdd); i++ {
		// Add a new page and set a bookmark at the current page
		pdf.AddPage()
		// Get the file name
		title := GetFileName(filesToAdd[i])
		pdf.Bookmark(title, 0, 0)
		
		_, lineHt := pdf.GetFontSize()
		// Add the file contents to the pdf
		contents := ReadFile(filesToAdd[i])
		pdf.Write(lineHt + 2, contents)
	}
	
	// pdf.AddPage()
	// pdf.SetFont("Arial", "B", 16)
	// pdf.Cell(40, 10, "Hello Captain Japan")

	// Alright now let's write the pdf to a file
	err := pdf.OutputFileAndClose(outputFile)

	if err != nil {
		panic(err)
	}
}

// Read the file and return it's contents. Also add a Title to the contents being returned.
// The title comes from the file name
func ReadFile(path string) string {
	// Open the file and get it's contents
	contents, err := os.ReadFile(path)
	// Check for errors
	if err != nil {
		panic(err)
	}

	// Ok let's add the title to the contents
	title := GetFileName(path)
	contents = append([]byte(title + "\n\n"), contents...)
	
	// Convet the contents to a string
	return string(contents)
}

// Get the name of a file from a absolute path
func GetFileName(path string) string {
	// Find the slash type
	var slashType string
	if strings.Contains(path, "/") {
		slashType = "/"
	} else {
		slashType = "\\"
	}

	// Split the path by the slash type
	pathSplit := strings.Split(path, slashType)

	// File name is last item in the split
	fileName := pathSplit[len(pathSplit)-1]
	// Now remove the extension
	fileName = strings.Split(fileName, ".")[0]

	return fileName
}

// Read the input passed in from the cmd
func ReadInput() []string {
	// Get the input
	argsWithoutProg := os.Args[1:]

	// Combine the input into one strings
	var input string
	for i := 0; i < len(argsWithoutProg); i++ {
		input += argsWithoutProg[i]
	}

	// Split the input by ";"
	inputSplit := strings.Split(input, ";")

	return inputSplit
}