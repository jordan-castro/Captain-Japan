#include <string>

using namespace std;

class Epub {
    public:
        Epub(string epubName);
        ~Epub();

        string getPath();
        string getName();

        /**
         * Creating a new XHTML file in the Text directory.
         */
        void addText(string filePath, string chapterTitle);
        /**
         * Creating a new image file in the Images directory
         */
        void addImage(string imagePath);

    private:
        void updateContent();
        void updateToc();

        string path;
        string name;
};  