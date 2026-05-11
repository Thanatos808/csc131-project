
public class MergeSort {

    // This is my Node class
    // Each node stores a value and a pointer to the next node
    // This is how  build the linked list from scratch
    static class Node {

        int data;
        Node next;

        Node(int data) {
            this.data = data;
            this.next = null;
        }
    }

    // This function prints my linked list
    //  use it to check if everything is built correctly
    public static void printList(Node head) {
        Node current = head;

        // move through the list until reach the end (null)
        while (current != null) {
            System.out.print(current.data + " -> ");
            current = current.next;
        }

        System.out.println("null");
    }

    // This is the merge function
    // It combines two sorted linked lists into one sorted list
    public static Node merge(Node a, Node b) {

        // If one list is empty,  just return the other one
        if (a == null) {
            return b;
        }
        if (b == null) {
            return a;
        }

        Node result;

        //  compare the values in both lists
        // and pick the smaller one each time
        if (a.data <= b.data) {

            //  attach the smaller node to my result
            result = a;
            // move forward in list A
            result.next = merge(a.next, b);
        } else {
            // Same idea, but now B is smaller
            result = b;
            // Move forward in list B
            result.next = merge(a, b.next);
        }

        return result;
    }

    // This function splits the linked list into two halves
    //  use slow and fast pointers to find the middle
    public static Node[] split(Node head) {

        // Base case: if list is empty or has one node, just return it
        if (head == null || head.next == null) {
            return new Node[]{head, null};
        }

        Node slow = head;
        Node fast = head.next;

        // Fast moves 2 steps, slow moves 1 step
        // When fast reaches the end, slow is at the middle
        while (fast != null) {
            fast = fast.next;

            if (fast != null) {
                slow = slow.next;
                fast = fast.next;
            }
        }

        // I split the list into two halves here
        Node a = head;        // left half starts at head
        Node b = slow.next;   // right half starts after middle

        // This breaks the list into two separate lists
        slow.next = null;

        return new Node[]{a, b};
    }

    // This is the merge sort function
    // It uses divide and conquer to sort the linked list
    public static Node mergeSort(Node head) {

        // Base case: if list is empty or has one node, it's already sorted
        if (head == null || head.next == null) {
            return head;
        }

        // I split the list into two halves
        Node[] parts = split(head);

        Node a = parts[0]; // left half
        Node b = parts[1]; // right half

        // recursively sort both halves
        a = mergeSort(a);
        b = mergeSort(b);

        //  merge the sorted halves back together
        return merge(a, b);
    }

    // Main method 
    public static void main(String[] args) {

        //  start with an array just to build my linked list
        int[] arr = {5, 1, 4, 2, 3};

        // Creating the head node using the first element
        Node head = new Node(arr[0]);
        Node current = head;

        //  loop through the array and build the linked list
        for (int i = 1; i < arr.length; i++) {
            current.next = new Node(arr[i]);
            current = current.next;
        }

        // Print original list before sorting
        System.out.println("Original List:");
        printList(head);

        // Call merge sort on the linked list
        head = mergeSort(head);

        System.out.println("Sorted List:");
        printList(head);
    }
}
