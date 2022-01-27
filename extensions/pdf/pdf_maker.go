package main

import (
	"encoding/json"
	"os"
	"strings"

	"github.com/jung-kurt/gofpdf"
)

func main() {
	// Get the path to the json file
	jsonPath := os.Args[1]
	// Get the files (pages) for the PDF
	pdfMaker := ReadJson(jsonPath)

	// Create the pdf
	pdf := gofpdf.New("P", "mm", "A4", "")
	pdf.SetAuthor("Captain Japan", true)

	output := pdfMaker["output"].(string)

	if pdfMaker["isManga"].(bool) {
		// Make a manga pdf
		chapters := pdfMaker["chapters"].(map[int]interface{})
		// Loop through the chapters
		for i := 0; i < len(chapters); i++ {
			// Get the chapter
			chapter := chapters[i].(map[string]interface{})
			title := chapter["title"].(string)
			pages := chapter["pages"].([]string)
			// Loop through the pages
			for j := 0; j < len(pages); j++ {
				if j == 1 {
					// Bookmark the previous chapter AKA (firs page of chapter)
					pdf.Bookmark(title, 0, 0)
					continue
				}
				// Add a page
				AddPage(pdf, true, pages[j])
			}
		}
	} else {
		chapter_array := pdfMaker["chapters"].([]interface{})
		var chapters []string
		for x := 0; x < len(chapter_array); x++ {
			chapters = append(chapters, chapter_array[x].(string))
		}
		
		// Loop through the chapters
		for i := 0; i < len(chapters); i++ {
			// Add a page
			AddPage(pdf, false, chapters[i])
		}
	}

	err := pdf.OutputFileAndClose(output)

	if err != nil {
		panic(err)
	}
}

// Add a page to the pdf
func AddPage(pdf *gofpdf.Fpdf, isManga bool, fileToAdd string) {
	// Add page
	pdf.AddPage()
	if !isManga {
		// Get the file name
		title := GetFileName(fileToAdd)
		// Add bookmark
		pdf.Bookmark(title, 0, 0)

		// Add the title to the pdf
		pdf.SetFont("Arial", "B", 16)
		pdf.Cell(40, 10, title)
		// Now reset the font
		pdf.SetFont("Arial", "", 12)

		_, lineHt := pdf.GetFontSize()
		// Add the file contents to the pdf
		contents := ReadFile(fileToAdd, false)
		pdf.Write(lineHt + 2, contents)
	} else {
		// name of image
		imageName := GetFileName(fileToAdd)
		// Register a image
		pdf.RegisterImageOptionsReader(imageName, gofpdf.ImageOptions{ImageType: "PNG"}, strings.NewReader(ReadFile(fileToAdd, true)))
		// Add a Image to the pdf
		pdf.ImageOptions(fileToAdd, 0, 0, -1, -1, false, gofpdf.ImageOptions{ImageType: "PNG"}, 0, imageName)
	}
}

// Read the file and return it's contents. Also add a Title to the contents being returned.
// The title comes from the file name
func ReadFile(path string, isManga bool) string {
	// Open the file and get it's contents
	contents, err := os.ReadFile(path)
	// Check for errors
	if err != nil {
		panic(err)
	}

	// If isManga is true then just return the contents
	if isManga {
		return string(contents)
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

// Read the JSON file.
func ReadJson(path string) map[string]interface{} {
	var jsonData interface{}

	// Read the data from the file
	contents, err := os.ReadFile(path)

	if err != nil {
		panic(err)
	}

	// Unmarshal the data
	err = json.Unmarshal([]byte(contents), &jsonData)
	if err != nil {
		panic(err)
	}

	return jsonData.(map[string]interface{})
}
