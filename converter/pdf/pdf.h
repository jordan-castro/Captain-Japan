#include <string>
#include <vector>

using namespace std;


class Pdf {
    public:
        Pdf(string name);
        ~Pdf();
        
        /**
         * The name of the pdf.
         */
        string name;
        /*
            The  path to the PDF. Comes from name.
        */
        string path;

        // void addImage();
        /*
            Add a new file to the pdf.

            Params:
                - `string filePath` The path to the file.
        */
        void addFile(string filePath);
        /*
            Build the PDF from the files passed in addFile.
        */
        void build();

    private:
        /*
            Combine the files that will become the PDF. 
        */
        void combineFiles();
        /*
            A tracker for the pdf files.
        */
        vector<string> currentFiles;
};