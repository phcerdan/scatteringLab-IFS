#include <iostream>
#include <string>
#include <stdio.h>
#include <windows.h>
#include <math.h>
#define FLEXMODE64 'A'    //Single mode
#define FLEXMODEQ 'B'     // Quad mode
#define FLEXMODED 'C'     // Dual mode
#define TIME_FLEX  0.052428799999999999999999999999547
#define FIRSTDELAY   1E-6/640
typedef void (__cdecl* USBSTART)(BYTE, WORD, BYTE, char *);  // Argument : 0 auto, 1: cross.
typedef void (__cdecl* USBSTOP)(void);
typedef BYTE (__cdecl* USBINITIALIZE)(BYTE); // Returns 1 if successful, 0 if not.
typedef BYTE (__cdecl* USBUPDATEUPDATE)(float *, unsigned short int *,
    			double *, double *, double *, double *, float *, float *, double *, double *);  // Return real time data, see example.
typedef void (__cdecl* USBFREE)(void); // Clean up.
using namespace std;
int main(int argc,  char** argv)
{
	int					i,j;
	float				ElapsedTime;
	unsigned short int	tracecnt;
	float				corr1[1120];
	float				corr2[624];
	float				corr3[304];
	float				corr4[304];
	float				DelayTime[1120];
	float				traceA[512];
	float				traceB[512];
	double				HistogramA[2048];
	double				HistogramB[2048];
	double				IntensityA, IntensityB;

	double				rawcorr[1248];  //The maximum is 624*2
	double				baseA[1248];
	double				baseB[1248];
	double				samples[1120];  // The maximum is 1120 in single mode

	FILE				*stream;
	HINSTANCE hDLL;               // Handle to DLL
	USBSTART Start;    // Function pointer
	USBSTOP Stop;    // Function pointer
	USBINITIALIZE Initialize;    // Function pointer
	USBUPDATEUPDATE Update;    // Function pointer
	USBFREE Usbfree;    // Function pointer

	BYTE mode;
	int					DurationTime;
	if (argc < 3) {
		cout << "mode options: single, quad, dual ; duration seconds" << endl;
		cout << ".exe 10 single" << endl;
		return 1;
	}
	string inputDurationTime = argv[1];
	DurationTime = stoi(inputDurationTime);
	string inputMode = argv[2];
	if (inputMode == "single") {
		mode = FLEXMODE64;
	}
	else if (inputMode == "quad") {
		mode = FLEXMODEQ;
	}
	else if (inputMode == "dual") {
		mode = FLEXMODED;
	}
	else {
		std::cout << "Mode unrecognized: " << inputMode << std::endl;
		return 1;
	}
	std::cout << "Duration Time: " + string(inputDurationTime) <<
		" ; Operating mode: " + string(inputMode) << std::endl;
// Calculate the delay times
	switch(mode)
	{
		case FLEXMODE64 :
			for(i=0;i<64;i++)
				DelayTime[i] = (i+1)*FIRSTDELAY;
			for(j=1;j<33;j++)
				for(i=0;i<32;i++)
					DelayTime[i+(j-1)*32+64] = DelayTime[(j-1)*32+64+i-1]+FIRSTDELAY*(float)pow(2,j);
			break;
		case FLEXMODED :
			for(i=0;i<32;i++)
				DelayTime[i] = (i+1)*FIRSTDELAY;
			for(j=1;j<37;j++)
				for(i=0;i<16;i++)
					DelayTime[i+(j-1)*16+32] = DelayTime[(j-1)*16+32+i-1]+FIRSTDELAY*(float)pow(2,j);
			break;
		case FLEXMODEQ :
			for(i=0;i<16;i++)
				DelayTime[i] = (i+1)*FIRSTDELAY;
			for(j=1;j<37;j++)
				for(i=0;i<8;i++)
					DelayTime[i+(j-1)*8+16] = DelayTime[(j-1)*8+16+i-1]+FIRSTDELAY*(float)pow(2,j);
			break;
	}

	hDLL = LoadLibrary("flex02-01dc_win7.dll");
	if (hDLL != NULL)
	{

	   Initialize = (USBINITIALIZE)GetProcAddress(hDLL,
											   "_USBInitialize");
	   if (!Initialize)
	   {
		  // handle the error
		  FreeLibrary(hDLL);
		  return 1;
	   }
	   Start = (USBSTART)GetProcAddress(hDLL,
											   "_USBStart");
	   if (!Start)
	   {
		  // handle the error
		  FreeLibrary(hDLL);
		  return 1;
	   }
	   Stop = (USBSTOP)GetProcAddress(hDLL,
											   "_USBStop");
	   if (!Stop)
	   {
		  // handle the error
		  FreeLibrary(hDLL);
		  return 1;
	   }
	   Update = (USBUPDATEUPDATE)GetProcAddress(hDLL,
											   "_USBUpdateRawdata");
	   if (!Update)
	   {
		  // handle the error
		  FreeLibrary(hDLL);
		  return 1;
	   }
	   Usbfree = (USBFREE)GetProcAddress(hDLL,
											   "_USBFree");
	   if (!Usbfree)
	   {
		  // handle the error
		  FreeLibrary(hDLL);
		  return 1;
	   }
	// Test the presence of the correlator
		if(Initialize(mode) == 1)
			cout << "The card is present" << endl;
		else
		{
			cout << "The card is not present" << endl;
			return 1;
		}


	// starts the correlator in autocorrelation mode
		Start(0, 80, 0, "test.dat");
		ElapsedTime = 0;
	//runs for DurationTime seconds
		while( ElapsedTime < DurationTime )
		{
			// Sleep for a second
			Sleep(1000);
			// Hello correlator
			if(Update(&ElapsedTime, &tracecnt, rawcorr, samples, baseA, baseB, traceA, traceB, HistogramA, HistogramB)==0)
			{
				cout << "The card is disconnected" << endl;
				return 1;
			}
				;
			// Calculate the average intensity for channel A
			IntensityA = 0;
			IntensityB = 0;
			if(tracecnt != 0)
			{
				for(i = 0; i<tracecnt; i++)
					IntensityA += traceA[i];
				IntensityA /= tracecnt*TIME_FLEX;
				for(i = 0; i<tracecnt; i++)
					IntensityB += traceB[i];
				IntensityB /= tracecnt*TIME_FLEX;
			}
			// Display it
			cout << "Intensities: " << IntensityA <<" ,"<< IntensityB << endl;
		}

	  //stops the correlator
		Stop();
	  //Clean up
		Usbfree();
		FreeLibrary(hDLL);
		// Display the final correlation function
		fopen_s(&stream, "corr.dat","wt");
		switch(mode)
		{
			case FLEXMODE64 :
				for(i = 0; i<1120; i++)
				{
					if((baseA[i] != 0) && (baseB[i] != 0))
						corr1[i] = rawcorr[i]*samples[i]/baseA[i]/baseB[i];
					else
						corr1[i] = 0;
					fprintf(stream, "%e,%e\n",DelayTime[i], corr1[i]);
				}
				break;
			case FLEXMODED :
				for(i = 0; i<624; i++)
				{
					if((baseA[i] != 0) && (baseB[i] != 0))
						corr1[i] = rawcorr[i]*samples[i]/baseA[i]/baseB[i];
					else
						corr1[i] = 0;
					if((baseA[i+624] != 0) && (baseB[i+624] != 0))
						corr2[i] = rawcorr[i+624]*samples[i]/baseA[i+624]/baseB[i+624];
					else
						corr2[i] = 0;
					fprintf(stream, "%e,%e,%e\n",DelayTime[i], corr1[i], corr2[i]);
				}
				break;
			case FLEXMODEQ :
				for(i = 0; i<304; i++)
				{
					if((baseA[i] != 0) && (baseB[i] != 0))
						corr1[i] = rawcorr[i]*samples[i]/baseA[i]/baseB[i];
					else
						corr1[i] = 0;
					if((baseA[i+304] != 0) && (baseB[i+304] != 0))
						corr2[i] = rawcorr[i+304]*samples[i]/baseA[i+304]/baseB[i+304];
					else
						corr2[i] = 0;
					if((baseA[i+304*2] != 0) && (baseB[i+304*2] != 0))
						corr3[i] = rawcorr[i+304*2]*samples[i]/baseA[i+304*2]/baseB[i+304*2];
					else
						corr3[i] = 0;
					if((baseA[i+304*3] != 0) && (baseB[i+304*3] != 0))
						corr4[i] = rawcorr[i+304*3]*samples[i]/baseA[i+304*3]/baseB[i+304*3];
					else
						corr4[i] = 0;
					fprintf(stream, "%e,%e,%e,%e,%e\n",DelayTime[i], corr1[i], corr2[i], corr3[i], corr4[i]);
				}
		}
		fclose(stream);
	} else { // load library null
	cout << "flex02-01dc_win7.dll library not found" << endl;
 }

	return 0;
}
