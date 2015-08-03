#include <stdio.h>
#include <pthread.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <malloc.h>
#include <limits.h>

int** dist;
int** nex;
FILE * ifp;

struct jloop_args
{
	int start;
	int end;
	int k;
	int len;
};

void *jloop(void *arg){
	struct jloop_args* jargs=arg;

	int start=jargs->start;
	int end=jargs->end;
	int k=jargs->k;
	int len=jargs->len;

	printf("%d,%d,%d,%d\n",start,end,k,len);

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

int main(){
ifp = fopen("data.csv", "r");
int num_nodes;
fscanf(ifp, "%d",&num_nodes);
printf("Edges: %d\n",num_nodes);
dist=malloc(sizeof(int*)*num_nodes);
nex=malloc(sizeof(int*)*num_nodes);

//Initalize our arrays.
for (int i = 0; i < num_nodes; ++i)
{
	dist[i]=malloc(sizeof(int)*num_nodes);
	nex[i]=malloc(sizeof(int)*num_nodes);
	for (int j = 0; j < num_nodes; ++j)
	{
		if (j != i){
			dist[i][j]=400000; //nowhere on campus is > 10km.; //cleaner than inf!
		}else{
			dist[i][j]=0;
		}
	}

}

printf("Finished mem allocation/initial sets \n");
int cnt_lns=0;
int n1,n2,cdst;
while (fscanf(ifp, "%d,%d,%d",&n1,&n2,&cdst) != EOF) {
//	printf("%d\n", cnt_lns);
	cnt_lns++;
	dist[n1][n2]=cdst;
	nex[n1][n2]=n2;
}

printf("Finished data import\n");
printf("Begin pre-thread calculations...\n");

int cnt=0;
int per_thread,last_thread;
if (num_nodes % 8 != 0){
	int extra= num_nodes % 8;
	per_thread=(num_nodes-extra)/8;
	last_thread=per_thread+extra;
	printf("nds: %d, ttl=%d, pt:%d, lt:%d\n",num_nodes,(per_thread*8)+last_thread,per_thread,last_thread);
}else{
	per_thread=num_nodes/8;
	last_thread=num_nodes/8;
}
printf("Begin workloop...\n");
for (int k = 0; k < num_nodes; ++k)
{
	printf("On: %d of %d\n",k+1,num_nodes);
	pthread_t pth[8];
	int curCnt=0;
	for (int i = 0; i < 7; ++i)
	{

			struct jloop_args *args = malloc(sizeof(struct jloop_args));
			args->start=curCnt;
			args->end=curCnt+per_thread;
			args->k=k;
			args->len=num_nodes;

			//printf("M: %d,%d,%d,%d\n",args[0],args[1],args[2],args[3]);
			pthread_create(&(pth[i]),NULL,jloop,(void*)args);
			curCnt+=per_thread;
			//printf("M2: %d,%d,%d,%d\n",args[0],args[1],args[2],args[3]);

	}

	struct jloop_args *args = malloc(sizeof(struct jloop_args));
	args->start=curCnt;
	args->end=num_nodes;
	args->k=k;
	args->len=num_nodes;
	pthread_create(&(pth[7]),NULL,jloop,(void*)args);
	for (int i = 0; i < 8; ++i)
	{
		pthread_join(pth[i],NULL);
		//printf("Tfinished:%d\n",i);
	}
}
printf("finished\n");
fclose(ifp);
//Cleanup.
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

for (int i = 0; i < num_nodes; ++i)
{
	free(dist[i]);
	free(nex[i]);

}
free(dist);
free(nex);

}
