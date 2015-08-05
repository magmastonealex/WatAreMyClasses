#include <stdio.h>
#include <pthread.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <malloc.h>
#include <limits.h>


#define NUM_THREADS 8
//Change the above if you have more or less cores available. Hyperthreaded cores WILL SLOW IT DOWN SIGNIFICANTLY!

/*

This is C code called by pfinder_t. Compile it using make in this directory.
*/
int** dist;
int** nex;
FILE * ifp;

struct jloop_args //Used as a thread-safe way to pass several arguments to threads.
{
	int start;
	int end;
	int k;
	int len;
};

//Runs the 2nd loop in batches.
//Takes a jloop_args as input.
// !!! frees the args upon completion!!!

void *jloop(void *arg){
	struct jloop_args* jargs=arg;

	int start=jargs->start;
	int end=jargs->end;
	int k=jargs->k;
	int len=jargs->len;

//	printf("%d,%d,%d,%d\n",start,end,k,len);

	for (int i = start; i < end; ++i)
	{
		for (int j = 0; j < len; ++j)
		{

			if ( ( (dist[i][k] + dist[k][j]) < dist[i][j] ) ) {
//				printf("d1: %d, d3:%d\n", dist[i][j],dist[i][k] +dist[k][j]);
				dist[i][j] = dist[i][k] + dist[k][j];
			//	printf("Setting dist %d-%d to %d\n", i,j,dist[i][j]);
				nex[i][j] = nex[i][k];
			}
		}
	}
	free(jargs);
}


//Opens, runs, writes.
int main(){
ifp = fopen("data.csv", "r"); // Open input data.
int num_nodes;
fscanf(ifp, "%d",&num_nodes);
printf("Edges: %d\n",num_nodes); // NODES is line #1.
dist=malloc(sizeof(int*)*num_nodes); //Allocate dist array 1st dimension
nex=malloc(sizeof(int*)*num_nodes); //Same for nex.

//Initalize our arrays.
for (int i = 0; i < num_nodes; ++i)
{
	dist[i]=malloc(sizeof(int)*num_nodes); // Allocate 2nd dimension.
	nex[i]=malloc(sizeof(int)*num_nodes); // Allocate 2nd dimension.
	for (int j = 0; j < num_nodes; ++j)
	{
		if (j != i){
			dist[i][j]=400000; //nowhere on campus is > 400km apart. I hope, at least.
						       //This was done to prevent overflow errors.
		}else{
			dist[i][j]=0; //Same node? 0 distance.
		}
	}

}

printf("Finished mem allocation/initial sets \n");
int cnt_lns=0; // Count the # of lines
int n1,n2,cdst; //Node 1, Node 2, distance between
while (fscanf(ifp, "%d,%d,%d",&n1,&n2,&cdst) != EOF) { // Effectively CSV format.
//	printf("%d\n", cnt_lns);
	cnt_lns++;
	dist[n1][n2]=cdst;
	nex[n1][n2]=n2; // Part of path-reconstruction.
}

printf("Finished data import\n");
printf("Begin pre-thread calculations...\n");


//Figure out the # of tasks to give each of the defined threads.
int cnt=0;
int per_thread,last_thread;
if (num_nodes % NUM_THREADS != 0){
	int extra= num_nodes % NUM_THREADS;
	per_thread=(num_nodes-extra)/NUM_THREADS;
	last_thread=per_thread+extra;
	printf("nds: %d, ttl=%d, pt:%d, lt:%d\n",num_nodes,(per_thread*NUM_THREADS)+last_thread,per_thread,last_thread);
}else{
	per_thread=num_nodes/NUM_THREADS;
	last_thread=num_nodes/NUM_THREADS;
}
//Outer loop & thread creation.
printf("Begin workloop...\n");
for (int k = 0; k < num_nodes; ++k)
{
	printf("On: %d of %d\n",k+1,num_nodes);
	pthread_t pth[NUM_THREADS]; 
	int curCnt=0;
	for (int i = 0; i < (NUM_THREADS-1); ++i)
	{

			struct jloop_args *args = malloc(sizeof(struct jloop_args)); // Dynamically allocate memory for EACH
			args->start=curCnt;											 // THREAD's arguments. Thread will free.
			args->end=curCnt+per_thread;
			args->k=k;
			args->len=num_nodes;

			pthread_create(&(pth[i]),NULL,jloop,(void*)args); // Create thread, casting args to a generic type.
			curCnt+=per_thread;

	}

	struct jloop_args *args = malloc(sizeof(struct jloop_args)); // Last one will take the rest.
	args->start=curCnt;											//Side effect of not erroring out if calculations
	args->end=num_nodes;										//above screw up.
	args->k=k;
	args->len=num_nodes;
	pthread_create(&(pth[NUM_THREADS-1]),NULL,jloop,(void*)args);
	for (int i = 0; i < NUM_THREADS; ++i)
	{
		pthread_join(pth[i],NULL); // Join each thread back to main once it's finished.
	}
}
printf("finished\n");
fclose(ifp);

//Output stage.

FILE * ofp; 
FILE * ofpnex;
ofp = fopen("dataout.csv", "w");
ofpnex = fopen("dataout-nex.csv", "w");

for (int k = 0; k < num_nodes; ++k){

	for (int i = 0; i < num_nodes; ++i){
		fprintf(ofp,",%d-%d",i,dist[k][i]);
		fprintf(ofpnex,",%d-%d",i,nex[k][i]);
	}
	fprintf(ofp,"\n");
	fprintf(ofpnex,"\n");
}

fclose(ofp);
fclose(ofpnex);

//Taking care of memory.

for (int i = 0; i < num_nodes; ++i)
{
	free(dist[i]);
	free(nex[i]);

}
free(dist);
free(nex);

}
