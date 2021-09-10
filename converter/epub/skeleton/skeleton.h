#include <vector>
#include <string>

using namespace std;

class EpubSkeleton {
    public:
        EpubSkeleton();
        ~EpubSkeleton();

        void buildSkeleton(string epubName);
        string getName();
        string getPath();

    private:
        void buildMetaInf();
        void buildOEPBS();
        void mimeType();

        string epubName;
        string epubPath;
};