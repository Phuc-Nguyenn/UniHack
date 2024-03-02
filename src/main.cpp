#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

const int fps = 20;

int main()
{
	Mat frame;
	VideoCapture vid(0);

	if( !vid.isOpened()) {
		return -1;
	}

	while ( vid.read(frame))
	{
		imshow("webcam", frame);

		if(waitKey (1000/fps) >= 0)
			break;
	}

	

	return 1;
}