/* BitCompression
This sample is provided as-is, without any warranty.

(c) 2007 ViALUX GmbH. All rights reserved.
*/

// BlackWhiteSample.cpp : Defines the entry point for the console application.
//

#include <TCHAR.h>
#include <windows.h>
#include <conio.h>
#include <stdio.h>
#include <stdlib.h>
#include "alp.h"
#include <iostream>
#include <string>
#include <dirent.h>
extern "C" int __fseeki64(FILE *, __int64, int);
//extern "C" __int64 __cdec1__ftelli64(FILE *);

int _tmain(int /*argc*/, _TCHAR** /* *argv[]*/)
{
	ALP_ID nDevId, nSeqId1, nSeqId2, nSeqId3;
	long nDmdType;
	__int64 nSizeX, nSizeY;
	long nReturn;
	//const long nPictureTime = 1000000;	// in µs
	UCHAR *pImageData = NULL;
	long nOffset = 1024;	// divide the frame LUT in 2



	FILE *file, *ordered;
	const char *filename, *filevec;
	int filesize;
	UCHAR *block1, *block2, *temp;

	long nCurrent;

	long nBit;
	long sortie;
	tAlpProjProgress QueueInfo;
	tFlutWrite LutArray;


	// Allocate the ALP high-speed device
	/* sortie = AlpDevAlloc( ALP_DEFAULT, ALP_DEFAULT, &nDevId);
	printf("%ld \n",sortie);
	_tprintf( _T("Press any key to stop ALP projection") );
	do { _getch(); } while (_kbhit()) ; */
	if (ALP_OK != AlpDevAlloc(ALP_DEFAULT, ALP_DEFAULT, &nDevId)) return 1;

	//SD : Reverses black into white. Caution : takes two frames to be complete
	//if (ALP_OK != AlpProjControl(nDevId, ALP_PROJ_INVERSION, 1)) printf("errorProjInv\n");

	// Inquire DMD type
	if (ALP_OK != AlpDevInquire(nDevId, ALP_DEV_DMDTYPE, &nDmdType)) return 1;
	switch (nDmdType) {
	case ALP_DMDTYPE_XGA_055A:
	case ALP_DMDTYPE_XGA_055X:
	case ALP_DMDTYPE_XGA_07A:
		nSizeX = 1024; nSizeY = 768;
		break;
	case ALP_DMDTYPE_DISCONNECT:
	case ALP_DMDTYPE_1080P_095A:
		nSizeX = 1920; nSizeY = 1080;
		break;
	case ALP_DMDTYPE_WUXGA_096A:
		nSizeX = 1920; nSizeY = 1200;
		break;
	default:
		// unsupported DMD type

		return 1;
	}


	//Prompt .bin and .vec filenames
	using namespace std;
	//	const string Binvec_Path = "g:/BINVECS/";
	//	const string Binvec_Path = "H:\BINVECS/";
	// const string Binvec_Path = "../../../BINVECS/";
	//const string Binvec_Path = "L:\BINVECS/";
	//	const string Binvec_Path = "../../../BINVECS/";// BINVECS / ";
	const string Binvec_Path = "E:\BINVECS/";
	cout << "Hello\n";
	DIR *dir;
	struct dirent *ent;
	if ((dir = opendir(Binvec_Path.c_str())) != NULL) {
		/* print all the files and directories within directory */
		ent = readdir(dir);
		ent = readdir(dir);
		int j = 0;
		while ((ent = readdir(dir)) != NULL) {
			printf("%d   %s\n", j, ent->d_name);
			j = j + 1;
		}
		closedir(dir);
	}
	else {
		/* could not open directory */
		perror("empty dir");
		return EXIT_FAILURE;
	}
	cout << "Enter your user number : ";
	int user;
	cin >> user;
	if ((dir = opendir(Binvec_Path.c_str())) != NULL) {
		ent = readdir(dir);
		ent = readdir(dir);
		int j = 0;
		while ((ent = readdir(dir)) != NULL && j< user) {
			j = j + 1;
		}
	}
	else {
		/* could not open directory */
		perror("");
		return EXIT_FAILURE;
	}
	printf("\n");
	const string user_name = (ent->d_name);
	printf("Welcome %s! \n", ent->d_name);
	closedir(dir);

	const string  Bin_Path = Binvec_Path + user_name + "/Bin/";
	const string  Vec_Path = Binvec_Path + user_name + "/Vec/";

	//printf ("%s", Bin_Path);


	if ((dir = opendir(Bin_Path.c_str())) != NULL) {
		/* print all the files and directories within directory */
		ent = readdir(dir);
		ent = readdir(dir);
		int j = 0;
		while ((ent = readdir(dir)) != NULL) {
			printf("%d   %s\n", j, ent->d_name);
			j = j + 1;
		}
		closedir(dir);
	}
	else {
		/* could not open directory */
		perror("empty dir");
		return EXIT_FAILURE;
	}


	cout << "Enter the number of a .bin file : ";
	int bin;
	cin >> bin;

	if ((dir = opendir(Bin_Path.c_str())) != NULL) {
		ent = readdir(dir);
		ent = readdir(dir);
		int j = 0;
		while ((ent = readdir(dir)) != NULL && j< bin) {
			j = j + 1;
		}
	}
	else {
		/* could not open directory */
		perror("empty dir");
		return EXIT_FAILURE;
	}
	printf("\n");

	string bin_name;
	bin_name = (ent->d_name);
	bin_name = Bin_Path + bin_name;
	printf("Chosen .bin file : %s\n", ent->d_name);
	closedir(dir);

	printf("\n");

	if ((dir = opendir(Vec_Path.c_str())) != NULL) {
		/* print all the files and directories within directory */
		ent = readdir(dir);
		ent = readdir(dir);
		int j = 0;
		while ((ent = readdir(dir)) != NULL) {
			printf("%d   %s\n", j, ent->d_name);
			j = j + 1;
		}
		closedir(dir);
	}
	else {
		/* could not open directory */
		perror("");
		return EXIT_FAILURE;
	}

	//cout << "You choosed the bin file" << bin << ".\n";
	cout << "Enter the number of a .vec file : ";
	int vec;
	cin >> vec;

	if ((dir = opendir(Vec_Path.c_str())) != NULL) {
		ent = readdir(dir);
		ent = readdir(dir);
		int j = 0;
		while ((ent = readdir(dir)) != NULL && j< vec) {
			j = j + 1;
		}
	}
	else {
		/* could not open directory */
		perror("");
		return EXIT_FAILURE;
	}
	printf("\n");
	string vec_name;
	vec_name = (ent->d_name);
	vec_name = Vec_Path + vec_name;
	printf("Chosen .vec file : %s\n", ent->d_name);
	closedir(dir);
	printf("\n");


	//prompt Frequency of refresh
	cout << "Enter the frame rate (in Hz) : ";
	double rate;
	cin >> rate;
	const long nPictureTime = 1.0 / rate * 1000000;
	printf("\n");

	//prompt for advanced features
	cout << "Advanced features (y/n) ? ";
	string adv;
	cin >> adv;
	printf("\n");


	double nF = 200;
	if (adv.compare("y") == 0){

		//prompt for nFrames
		cout << "Number of frames in the LUT (usually 500) ? ";
		cin >> nF;
		printf("\n");

		//Prompt the bit depth
		/*	cout << "Enter the bit depth (8 unless you want to go to high speeds) : ";
		double bitDepth;
		cin >> bitDepth;
		nBit = bitDepth;
		printf("\n");*/
	}
	const long nFrames = nF;		// max 43690 binary frames

	////////////////////////////////////////////////////////////////////////////////////////////
	//Read Vec file

	long int temp1, temp2, temp3, temp4, temp5;

	//filevec="compte2.vec";
	filevec = vec_name.c_str();

	__int64	numberOfVecFrames = 0;

	file = fopen(filevec, "r");
	if (file == NULL) {
		printf("Invalid file name. \n");
	}
	printf("File Vec opened. \n");

	fscanf(file, "%ld %ld %ld %ld %ld", &temp1, &temp2, &temp3, &temp4, &temp5);

	while (fscanf(file, "%ld %ld %ld %ld %ld", &temp1, &temp2, &temp3, &temp4, &temp5) != EOF)
	{
		numberOfVecFrames++;
	}
	//numberOfVecFrames = 40 * 3600 * 1;
	printf("NbFramesPlayed = %d. \n", numberOfVecFrames);
	rewind(file);
	fscanf(file, "%ld %ld %ld %ld %ld", &temp1, &temp2, &temp3, &temp4, &temp5);

	__int64 * FrameNumbers = new __int64[numberOfVecFrames];
	int i = 0;
	while (fscanf(file, "%ld %ld %ld %ld %ld", &temp1, &temp2, &temp3, &temp4, &temp5) != EOF)
	{
		FrameNumbers[i] = temp2;
		i++;
	}
	fclose(file);


	long Nloop, Nremain;
	Nloop = numberOfVecFrames / (nOffset * 2);
	Nremain = numberOfVecFrames % (nOffset * 2);

	printf("Nloop = %d, Nremain = %d \n", Nloop, Nremain);


	/////////////////////////////////////////////////////////////////////////////////////


	// Read .bin header

	// filename
	//filename="compte.bin";
	filename = bin_name.c_str();

	// open file
	file = fopen(filename, "rb");
	if (file == NULL)
	{
		printf("Failed to open file for read access.");
	}

	//check file size
	_fseeki64(file, 0L, SEEK_END);
	filesize = ftell(file);
	rewind(file);

	// read header
	short header[4];
	fread(header, sizeof(short), 4, file);
	printf("header SizeX = %d, SizeY =  %d, NbFrames = %d . \n", header[0], header[1], header[2]);
	printf("Filesize : %d ", filesize);

	int header_size = sizeof(short)* 4;

	printf("OK1");

	// SD: the display window will be placed at the middle of the DMD screen
	nBit = header[3];
	int width = header[0] / 8 * nBit;
	int height = header[1];

	//SD: this trick allows to read compact movies, generated at the bit level. This compression is made at the expense of the gray level precision.
	int nSizeX_bit_trick = nSizeX / 8 * nBit;

	// SD: coordinates of the display window
	int beg_w = (nSizeX_bit_trick - width) / 2;
	//int end_w = beg_w + width;
	int beg_h = (nSizeY - height) / 2;
	//int end_h = beg_h + height;

	/////////////////////////////////////////////////////////////////////////////////////

	// SEQ 1 Allocate a first sequence of nFrames
	if (ALP_OK != AlpSeqAlloc(nDevId, nBit, nFrames, &nSeqId1)) printf("errorSeqAlloc\n");	//8bit

	printf("buffer size %d", nFrames*nSizeX_bit_trick*nSizeY);

	// buffer
	block1 = NULL;
	block1 = (UCHAR *)calloc(nFrames*nSizeX_bit_trick*nSizeY, 1);

	if (block1 == NULL)
	{
		printf("Failed to read data 1.\n");
	}

	// read file
	for (int i = 0; i<nFrames; i++)
	{
		//printf("Writing frame %d \n",FrameNumbers[i]);
		_fseeki64(file, FrameNumbers[i] * width*height + header_size, SEEK_SET);
		// SD: the display window is located at the center of the screen of the DMD
		for (int line = 0; line < height; line++){
			fread(block1 + i*(nSizeX_bit_trick*nSizeY) + (beg_h + line)*nSizeX_bit_trick + beg_w, 1, width, file);
		}
	}


	// Set up image timing
	//if (ALP_OK != AlpSeqControl(nDevId, nSeqId1, ALP_BITNUM, nBit)) printf("errorBinaryMode\n");
	if (nBit == 1){
		if (ALP_OK != AlpSeqControl(nDevId, nSeqId1, ALP_DATA_FORMAT, ALP_DATA_BINARY_TOPDOWN)) printf("errorBinaryMode3\n");
	}
	if (ALP_OK != AlpSeqTiming(nDevId, nSeqId1, ALP_DEFAULT, nPictureTime,
		ALP_DEFAULT, ALP_DEFAULT, ALP_DEFAULT)) return 1;

	/////////////////////////////////////////////////////////////////////////////////////
	// SEQ 2 Allocate a second sequence of nFrames

	printf("OK1");
	if (ALP_OK != AlpSeqAlloc(nDevId, nBit, nFrames, &nSeqId2)) printf("errorSeqAlloc\n");	//8bit

	// Read more frames

	// buffer
	block2 = NULL;
	block2 = (UCHAR *)calloc(nFrames*nSizeX_bit_trick*nSizeY, 1);

	if (block2 == NULL)
	{
		printf("Failed to read data 2.\n");
	}

	// read file
	for (int i = nFrames; i<2 * nFrames; i++)
	{
		//printf("Writing frame %d \n",FrameNumbers[i]);
		_fseeki64(file, (FrameNumbers[i])*width*height + header_size, SEEK_SET);
		for (int line = 0; line < height; line++){
			fread(block2 + (i - nFrames)*(nSizeX_bit_trick*nSizeY) + (beg_h + line)*nSizeX_bit_trick + beg_w, 1, width, file);
		}
	}


	// Set up image timing
	if (nBit == 1){
		if (ALP_OK != AlpSeqControl(nDevId, nSeqId2, ALP_DATA_FORMAT, ALP_DATA_BINARY_TOPDOWN)) printf("errorBinaryMode3\n");
	}
	if (ALP_OK != AlpSeqTiming(nDevId, nSeqId2, ALP_DEFAULT, nPictureTime,
		ALP_DEFAULT, ALP_DEFAULT, ALP_DEFAULT)) return 1;


	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	/// PLAY ON DMD
	printf("OK2");
	//Set up queue mode
	if (ALP_OK != AlpProjControl(nDevId, ALP_PROJ_QUEUE_MODE, ALP_PROJ_SEQUENCE_QUEUE)) return 1;
	printf("OK3");
	// Transmit images into ALP memory
	nReturn = AlpSeqPut(nDevId, nSeqId1, ALP_DEFAULT, ALP_DEFAULT, block1);
	if (ALP_OK != nReturn) return 1;
	printf("OK4");
	// Start Sequence 1 in queue mode
	if (ALP_OK != AlpProjStart(nDevId, nSeqId1)) return 1;
	_tprintf(_T("Seq1 \n"));
	printf("OK5");
	// Transmit images into ALP memory
	nReturn = AlpSeqPut(nDevId, nSeqId2, ALP_DEFAULT, ALP_DEFAULT, block2);
	if (ALP_OK != nReturn) return 1;
	printf("OK6");
	// Start sequence 2
	if (ALP_OK != AlpProjStart(nDevId, nSeqId2)) return 1;
	_tprintf(_T("Seq2 \n"));

	_tprintf(_T("infernal loop start \n"));

	int ts = 30;
	long j = 2 * nFrames;

	while (j<numberOfVecFrames)
	{	/////////////////////// SEQ1


		//fread(block1,1,nFrames*nSizeX*nSizeY,file);

		i = 0;
		while (i<nFrames && j<numberOfVecFrames)
		{
			//printf("Writing frame %d \n",FrameNumbers[j]);
			_fseeki64(file, (FrameNumbers[j])*width*height + header_size, SEEK_SET);
			for (int line = 0; line < height; line++){
				fread(block1 + i*(nSizeX_bit_trick*nSizeY) + (beg_h + line)*nSizeX_bit_trick + beg_w, 1, width, file);
			}
			i++;
			j++;
		}

		/// test sequence in play
		AlpProjInquireEx(nDevId, ALP_PROJ_PROGRESS, &QueueInfo);
		printf("SeqID = %d , Queue NWaiting = %d, Nframes = %d . \n", QueueInfo.SequenceId, QueueInfo.nWaitingSequences, QueueInfo.nFramesPerSubSequence);

		while (QueueInfo.nWaitingSequences >= 1 || QueueInfo.SequenceId == 0)
		{
			if (QueueInfo.SequenceId == 0)
				printf("Bug with AlpProjInquireEx: I will try again \n");
			AlpProjInquireEx(nDevId, ALP_PROJ_PROGRESS, &QueueInfo);
			Sleep(ts);
		}


		AlpProjControl(nDevId, ALP_PROJ_RESET_QUEUE, ALP_DEFAULT);
		printf("Seq 1 Finished . \n");

		if (_kbhit()) break;

		// Free Seq1
		nReturn = AlpSeqFree(nDevId, nSeqId1);
		_tprintf(_T(" ALP STATUS %d \n"), nReturn);

		//Reallocate Sequence 1
		if (ALP_OK != AlpSeqAlloc(nDevId, nBit, nFrames, &nSeqId1)) printf("errorSeqAlloc\n"); // 1bit
		_tprintf(_T("okalloc \n"));

		// Set up image timing
		if (nBit == 1){
			if (ALP_OK != AlpSeqControl(nDevId, nSeqId1, ALP_DATA_FORMAT, ALP_DATA_BINARY_TOPDOWN)) printf("errorBinaryMode3\n");
		}
		if (ALP_OK != AlpSeqTiming(nDevId, nSeqId1, ALP_DEFAULT, nPictureTime,
			ALP_DEFAULT, ALP_DEFAULT, ALP_DEFAULT)) return 1;

		// Transmit images into Seq1
		nReturn = AlpSeqPut(nDevId, nSeqId1, ALP_DEFAULT, ALP_DEFAULT, block1);
		_tprintf(_T(" ALP STATUS %d \n"), nReturn);

		// Start Sequence 1 in queue mode
		if (ALP_OK != AlpProjStart(nDevId, nSeqId1)) return 1;
		_tprintf(_T("Seq1 \n"));


		if (_kbhit()) break;

		///////////////// SEQ2

		//fread(block2,1,nFrames*nSizeX*nSizeY,file);
		i = 0;
		while (i<nFrames && j<numberOfVecFrames)
		{
			//printf("Writing frame %d \n",FrameNumbers[j]);
			_fseeki64(file, (FrameNumbers[j])*width*height + header_size, SEEK_SET);
			for (int line = 0; line < height; line++){
				fread(block2 + i*(nSizeX_bit_trick*nSizeY) + (beg_h + line)*nSizeX_bit_trick + beg_w, 1, width, file);
			}
			i++;
			j++;
		}

		AlpProjInquireEx(nDevId, ALP_PROJ_PROGRESS, &QueueInfo);
		printf("SeqID = %d , Queue NWaiting = %d, Nframes = %d . \n", QueueInfo.SequenceId, QueueInfo.nWaitingSequences, QueueInfo.nFramesPerSubSequence);

		while (QueueInfo.nWaitingSequences >= 1 || QueueInfo.SequenceId==0)
		{
			if (QueueInfo.SequenceId == 0)
				printf("Bug with AlpProjInquireEx: I will try again \n");
			AlpProjInquireEx(nDevId, ALP_PROJ_PROGRESS, &QueueInfo);
			Sleep(ts);
		}


		AlpProjControl(nDevId, ALP_PROJ_RESET_QUEUE, ALP_DEFAULT);
		printf("Seq 2 Finished . \n");

		if (_kbhit()) break;

		// Free Seq2
		nReturn = AlpSeqFree(nDevId, nSeqId2);
		_tprintf(_T(" ALP STATUS %d \n"), nReturn);


		//Reallocate Sequence 2
		if (ALP_OK != AlpSeqAlloc(nDevId, nBit, nFrames, &nSeqId2)) printf("errorSeqAlloc\n"); // 1bit
		_tprintf(_T("okalloc \n"));

		// Set up image timing
		if (nBit == 1){
			if (ALP_OK != AlpSeqControl(nDevId, nSeqId2, ALP_DATA_FORMAT, ALP_DATA_BINARY_TOPDOWN)) printf("errorBinaryMode3\n");
		}
		if (ALP_OK != AlpSeqTiming(nDevId, nSeqId2, ALP_DEFAULT, nPictureTime,
			ALP_DEFAULT, ALP_DEFAULT, ALP_DEFAULT)) return 1;

		// Transmit images into Seq2
		nReturn = AlpSeqPut(nDevId, nSeqId2, ALP_DEFAULT, ALP_DEFAULT, block2);
		_tprintf(_T(" ALP STATUS %d \n"), nReturn);

		// Start Sequence 2 in queue mode
		if (ALP_OK != AlpProjStart(nDevId, nSeqId2)) return 1;
		_tprintf(_T("Seq2 \n"));

		if (_kbhit()) break;

	}

	// Wait for key stroke
	_tprintf(_T("Press any key to stop ALP projection"));
	do { _getch(); } while (_kbhit());

	// Done
	AlpDevHalt(nDevId);
	AlpDevFree(nDevId);

	fclose(file);
	return 0;
}

