public class LabSorting {

    public static void main(String[] args) {

        // Bubble Sort 
        // reset array first, the sort based on 1st column, then prints results 
        SortSearch.resetArray();
        SortSearch.bubbleSort();
        System.out.println("After Bubble Sort (Column 1 Ascending)");
        SortSearch.printArray();

        // Selection Sort 
        // sort column 2 desending print results 
        SortSearch.resetArray();
        SortSearch.selectionSort();
        System.out.println("\nAfter Selection Sort (Column 2 Descending)");
        SortSearch.printArray();

        // Shell Sort
        // sofrt column 3 ascemnding, print results 
        SortSearch.resetArray();
        SortSearch.shellSort();
        System.out.println("\nAfter Shell Sort (Column 3 Ascending)");
        SortSearch.printArray();

        // Insertion Sort
        //sort row 5 ascending, print results 
        SortSearch.resetArray();
        SortSearch.insertionSort();
        System.out.println("\nAfter Insertion Sort (Row 5 Ascending)");
        SortSearch.printArray();

        // Binary Search
        // Ask user for a number in row 4 , print entire column if found 
        SortSearch.binarySearch();
    }
}
    