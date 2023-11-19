#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>

const int32_t maxWordSize = 100;
const int32_t maxTrackerSize = UINT16_MAX;

struct word_count {
    char word[maxWordSize];
    int32_t count;
};

// comparator function for comparing 2 elements
int compare_word_count(const void * a, const void * b){
    const struct word_count *wordCountA = (const struct word_count *)a;
    const struct word_count *wordCountB = (const struct word_count *)b;

    if (wordCountA->count < wordCountB->count) {
        return 1;
    }
    if (wordCountA->count == wordCountB->count) {
        return 0;
    }
    return -1;
}
char** find_frequent_words(const char *path, int32_t n) {
    FILE *fptr;
    // dynamically allocate the array of word
    char** result = malloc(n * sizeof(char*));
    for (int i = 0; i < n; ++i) {
        result[i] = malloc(maxWordSize * sizeof(char));
    }

    // opening the file in read mode
    fptr = fopen(path, "r");

    // check if the file opens successfully
    if (fptr == NULL) {
        printf("The file is not opened.");
        exit(0);
    }

    struct word_count wordTracker[maxTrackerSize];
    int wordTrackerSize = 0;

    char word[maxWordSize];
    // take in each word from the shakespeare.txt
    while (fscanf(fptr, "%s", word) == 1) {
        // Check for duplicates in wordTracker
        char isDuplicate = '0';

        // delete the non-alpha charcter at the end of the word
        int offset = 1;
        while (isalpha(word[strlen(word) - offset]) == 0 && ((int)strlen(word) - offset)>=0){
            word[strlen(word) - offset] = '\0' ;
            ++offset;
        }

        // if after deletion the word becomes empty, we skip executing the code below
        if (strlen(word) == 0){
            continue;
        }
        for (int i = 0; i < wordTrackerSize; ++i) {
            // if the 2 word equal one another (case insensitive)
            // we increment the count by one
            if (strcasecmp(word, wordTracker[i].word) == 0) {
                isDuplicate = '1';
                wordTracker[i].count++;
                break;
            }
        }

        // if we have not seen the word before, we put the word into the wordTracker
        if (isDuplicate == '0') {
            strcpy(wordTracker[wordTrackerSize].word, word);
            wordTracker[wordTrackerSize].count = 1;
            wordTrackerSize++;
        }
    }

    // close the file
    fclose(fptr);
    
    // sort the function based on the most frequent appearnace
    qsort(wordTracker, wordTrackerSize, sizeof(struct word_count), compare_word_count);

    // debug 
    for (int i = 0; i < n; ++i) {
        printf("Word: %s Count: %u\n", wordTracker[i].word, wordTracker[i].count);
    }

    // put the top most frequent n word into the result array
    for (int i = 0; i < n; ++i) {
        strcpy(result[i], wordTracker[i].word);
    }
    return result;
}

int main() {
    // ASSUMPTION: a word count as a word when we hit white space / end of line. 
    //Will also delete any non-alpha character at the end of the word. 
    const char *input = "shakespeare.txt";

    // assume we find the top 5 frequent word
    char ** array = find_frequent_words(input, 5);
    
    // free up the dynamically allocated space
    for (int i = 0; i < 5; ++i) {
        free(array[i]);
    }
    free(array);

    return 0;
}
