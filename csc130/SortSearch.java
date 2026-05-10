
import java.util.Scanner;

public class SortSearch {
// Original array to be sorted and searched

    static int[][] original
            = {
                {5, 3, 2, 16},
                {9, 8, 10, 17},
                {4, 7, 11, 18},
                {2, 5, 9, 12},
                {7, 9, 4, 10},};

    static int[][] arr = new int[5][4];  // Working array that will be sorted and searched

    static Scanner input = new Scanner(System.in); // Scanner object to get user input for binary search
// coppies the original array to the working array, allowing to reset the working array to its original state before each 
// sort or search operation.

    public static void resetArray() { // coppies original array into the working aarray before any sorting 

        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 4; j++) {
                arr[i][j] = original[i][j];
            }
        }
    }

    public static void printArray() {

        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 4; j++) {
                System.out.print(arr[i][j] + " "); // prints the current state of the 2D array in 5x 4 column format 
            }
            System.out.println();
        }
    }
// bubble sort() algorithm on the first column (ascending order) Entire rows move together while comparing based on the 
//first column values 

    public static void bubbleSort() {
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4 - i; j++) {
                if (arr[j][0] > arr[j + 1][0]) {
                    int[] temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;

                }
            }
        }
    }

    // Selection sort algorithm on the 2nd column (descending order)
    // Finds the maximum in the remaining rows and swaps
    public static void selectionSort() {
        for (int i = 0; i < 4; i++) {
            int max = i;
            for (int j = i + 1; j < 5; j++) {
                if (arr[j][1] > arr[max][1]) {
                    max = j;
                }
            }
            int[] temp = arr[i];
            arr[i] = arr[max];
            arr[max] = temp;
        }
    }
//Shell sort algorithm on the 3rd column (ascending order)
    // Uses gap sequence to sort more efficiently than insertion sort

    public static void shellSort() {
        for (int gap = 5 / 2; gap > 0; gap /= 2) {
            for (int i = gap; i < 5; i++) {
                int[] temp = arr[i];
                int j = i;
                while (j >= gap && arr[j - gap][2] > temp[2]) {
                    arr[j] = arr[j - gap];
                    j -= gap;

                }
                arr[j] = temp;
            }
        }
    }
// Searches for a user provided number in the 5th row using binary search, if found print sthe entire, column where number is 
//located 

    public static void insertionSort() {
        int row = 4; // fifth row
        for (int i = 1; i < 4; i++) { // columns 1 to 3
            int key = arr[row][i];
            int j = i - 1;
            // Move elements in the row to the right if greater than key
            while (j >= 0 && arr[row][j] > key) {
                arr[row][j + 1] = arr[row][j];
                j--;
            }
            arr[row][j + 1] = key;
        }
    }
// Searches for a user provided number in the 5th row using binary search, if found print the entire column where number is located

    public static void binarySearch() {
        System.out.print("\nWhat number are you searching for in the 5th row? ");
        int target = input.nextInt();
        int row = 4;
        int left = 0;
        int right = 3;
        while (left <= right) {

            int mid = (left + right) / 2;

            if (arr[row][mid] == target) {

                System.out.println("\nColumn containing " + target + ":");
                for (int i = 0; i < 5; i++) {
                    System.out.println(arr[i][mid]);
                }
                return;
            }
            if (arr[row][mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        System.out.println("Number not found.");
    }
}
