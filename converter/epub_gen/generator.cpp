#include "epub.h"

int main() {
    Epub epub = Epub("The begining after the end");
    epub.addText("C:\\Users\\jorda\\Documents\\Python_Projects\\Captain_Japan\\backend\\scraped_data\\novels\\the_beginning_after_the_end\\Chapter_1.html", "Chapter1");
    return 0;
}