
import java.io.*;
import java.util.*;
// Node class represents each element in the doubly linked list 
class Node {

    String name; // data stored in the node
    Node next; // pointer to the next node 
    Node prev; // pointer to the previous node 

    public Node(String name) { // constructor to initialize a node with a name 
        this.name = name; 
        this.next = null;
        this.prev = null;
    }
}
// Main class for the doubly linked list p
public class DoublyLinkedListProgram {
// Head points to the first node in the list 
   private Node head;
// Tail points to the last node in the list 
   private Node tail;

    public DoublyLinkedListProgram() { // Constructor to initialize an empty list
        head = null;
        tail = null;
    }
// Inserts a new node in the list while maintaining sorted alphabetical order based on the name
    public void insert(String data) {
        data = data.toLowerCase(); // converts to lowercase 
// creates a new node with the provided data
        Node newNode = new Node(data);

// 1: if the node is empty the new node becomes both the head and tail of the list
        if (head == null) {
            head = tail = newNode;
// 2: insert at the beginning if the new value is smaller than head 
        } else if (data.compareTo(head.name) < 0) { // insert at the head
            newNode.next = head; // new node points to the current head
            head.prev = newNode; // old head points back to the new node
            head = newNode; // update head to the new node
 // 3: insert at the end if the new value is greater than tail
        } else if (data.compareTo(tail.name) > 0) { // insert at the tail
            tail.next = newNode; // old tail points to the new node
            newNode.prev = tail; // new node points back to the old tail
            tail = newNode;     // update tail to the new node
// 4: insert in the middle if the new value is between head and tail 
        } else { 
            Node current = head;
            // Traverse the list until the correct sorted posisiton is found 
            while (current != null && data.compareTo(current.name) > 0) {
                current = current.next;
            }
            // Adjust the pointers to insert the new node two existing nodes 
            newNode.next = current;
            newNode.prev = current.prev;
            current.prev.next = newNode;
            current.prev = newNode;
        }
    }
// deletes a node from the list based on the name provided 
    public void delete(String data) { // delete a node by name 
        data = data.toLowerCase(); // converts to lowercase 

        Node current = head;
// Traverse the list to find the node with the matching name       
        while (current != null && !current.name.equals(data)) {
            current = current.next;
        }
 // if the node was not found return        
        if (current == null) {
            return;
        }
// 1: Only one node in the list 
        if (current == head && current == tail) {
            head = tail = null;
// 2: Deleting the head node 
        } else if (current == head) { // move the head forward 
            head = head.next;
            if (head != null) head.prev = null; // remove backward refrence 
 // 3: Deleting the tail node
        } else if (current == tail) { 
            tail = tail.prev; // move the tail backward
            tail.next = null; // remove forward reference
// 4: Deleting a node in the middle            
        } else {
            current.prev.next = current.next; // link previous node to next node
            current.next.prev = current.prev; // link next node to previous node 
        }
    }

// Traverse the list from the head to tail and writes the results to a file 
// display the list in descending and acscending order
    public void displayAscendingToFile(PrintWriter out) {
        Node current = head;
        while (current != null) { // continue until the end of the list is reached
            out.println(current.name);
            current = current.next;
        }
    }
// Traverses the list from tail to head 
    public void displayDescendingToFile(PrintWriter out) {
        Node current = tail;
        while (current != null) { // moves backward through the list until the beginning is reached
            out.println(current.name);
            current = current.prev;
        }
    }

// Maain method to read from input file, process the data, and write results to output file
    public static void main(String[] args) throws Exception {
        DoublyLinkedListProgram list = new DoublyLinkedListProgram(); // created a new doubly linked list 

        Scanner file = new Scanner(new File("input.txt")); // open input file containing names and delete commands 
        while (file.hasNext()) { // read file line by line 
            String line = file.nextLine().trim();
            if (line.length() == 0) continue;  // skips blank lines 

            if (line.toLowerCase().startsWith("delete ")) {  // if the line begins with "delete", remove speicified name 
                String name = line.substring(7).trim();  // extract the name after word delete 
                list.delete(name);
            // else insert the name into the list in sorted order
            } else { 
                list.insert(line);
            }
        }
        // close the input file 
        file.close();

        // create output file 
        PrintWriter out = new PrintWriter(new File("output.txt"));
        list.displayAscendingToFile(out); // print list in ascending order to the output file
        out.println("================================");
        list.displayDescendingToFile(out); // print list in descending order to the output file
        out.close(); // close output file 
     
        System.out.println("Processsing complete. Check output.txt for results.");
    }

}
