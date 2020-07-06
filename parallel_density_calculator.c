#include <stdio.h>
#include <omp.h>
#include <stdlib.h>

#define THREADS 8

typedef short bool;

int f1, f2;
int n = 10 * 1000;
int t_trans = 5 * 1000;
unsigned int seeds[THREADS];


bool f(int rule,bool x,bool y, bool z) {
    return (rule >> ( x * 4 + y * 2 +z) & 1);
}

bool *simulate(double lambda, int *seed) {
    bool *state = (bool *) malloc(n * sizeof(bool));
    bool *state_old = (bool *) malloc(n * sizeof(bool));

    for(int i=0; i<n; i++) {
        int r = rand_r(seed); 
        state_old[i] = (r < RAND_MAX / 2) ? 1 : 0;
        //printf("%s", state[i] == 1 ? "#" : " ");
    }
    //printf("\n");

    for (int t = 0; t < t_trans; t++) {
        for (int i = 0; i < n; i++) {
            //printf("lambda = %f, t = %i\n", lambda, t);
            bool x = state_old[(i-1) % n];
            bool y = state_old[i % n];
            bool z = state_old[(i+1) % n];

            double r = rand_r(seed) / (double) RAND_MAX;
            state[i] = (r > lambda) ? f(f1,x,y,z) : f(f2,x,y,z);
            //printf("%s", state[i] == 1 ? "#" : " ");
        }
        //printf("\n");
        bool *temp;
        temp = state;
        state = state_old;
        state_old = temp;
    }


    free(state_old);

    return state;
}

double get_density(bool *state) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += state[i];
    }

    return (double) sum / (double) n;
}

double get_kink_density(bool *state) {
    int i = 0,j=1;

    int sum = 0;

    while (j < n) {

        if(state[i] != state[j]) sum += 1;

        i++;
        j++;
    }

    return (double) sum / (double) n;

}

int main(int argc, char **argv) {
    omp_set_num_threads(THREADS);
    f1 = atoi(argv[1]);
    f2 = atoi(argv[2]);

    // Initialize seed for each thread
    FILE* r = fopen("/dev/urandom", "r");
    if (fread(seeds, sizeof(seeds), 1, r) != 1) {
        fprintf(stderr, "Could not intialize random number generator");
    }
    fclose(r);

    const int lambdas[] = {1,2,3,4,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,96,97,98,99,100};
    const int num_lambdas = sizeof(lambdas) / sizeof(int);

    printf("lambda,density,kink_density\n");
#pragma omp parallel for
    for (int i = 0; i < num_lambdas; i++) {
        int seed = seeds[omp_get_thread_num()];
        double my_lambda = (double) lambdas[i] / 100.0;
        bool *state = simulate(my_lambda, &seed);
        double my_density = get_density(state);
        double my_kink_density = get_kink_density(state);

        printf("%f,%f,%f\n", my_lambda, my_density, my_kink_density);
        free(state);

    }
}
