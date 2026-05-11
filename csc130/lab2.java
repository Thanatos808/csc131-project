
import java.util.Scanner;

class Node<T> {

    T data;
    Node<T> next;

    Node(T data) {
        this.data = data;
        this.next = null;
    }
}

class Stack<T> {

    private Node<T> top;

    public void push(T value) {
        Node<T> newNode = new Node<>(value);
        newNode.next = top;
        top = newNode;

    }

    public T pop() {
        T value = top.data;
        top = top.next;
        return value;
    }

    public T peek() {
        return top.data;
    }

    public boolean isEmpty() {
        return top == null;
    }

}

class Queue<T> {

    private Node<T> front;
    private Node<T> rear;

    public void enqueue(T value) {
        Node<T> newNode = new Node<>(value);
        if (rear != null) {
            rear.next = newNode;
        }
        rear = newNode;
        if (front == null) {
            front = rear;
        }
    }

    public T dequeue() {
        T value = front.data;
        front = front.next;
        if (front == null) {
            rear = null;
        }
        return value;

    }

    public boolean isEmpty() {
        return front == null;
    }

}

class Postfix // precedence of operators
{

    public static int precedence(char operator) {
        switch (operator) {
            case '=':
                return 1;
            case '(':
                return 2;
            case '+':
            case '-':
                return 3;
            case '*':
            case '/':
                return 4;

        }
        return 0;
    }

    // covert infix to postfix
    public static String convert(String infix) {

        Stack<Character> stack = new Stack<>();
        Queue<Character> output = new Queue<>();

        for (int i = 0; i < infix.length(); i++) {
            char ch = infix.charAt(i);

            // if number 
            if (Character.isDigit(ch)) {
                output.enqueue(ch);
            } // if open prenthesis
            else if (ch == '(') {
                stack.push(ch);
            } // if close parenthesis 
            else if (ch == ')') {
                while (!stack.isEmpty() && stack.peek() != '(') {
                    output.enqueue(stack.pop());
                }
                stack.pop(); // remove '(' from stack

            } // if operator 
            else {
                while (!stack.isEmpty() && precedence(ch) <= precedence(stack.peek())) {
                    output.enqueue(stack.pop());
                }
                stack.push(ch);
            }
        }
        while (!stack.isEmpty()) {
            output.enqueue(stack.pop());
        }
        // convert queue to string
        String postfix = "";
        while (!output.isEmpty()) {
            postfix += output.dequeue();
        }
        return postfix;
    }

    public static int evaluate(String postfix) {
        Stack<Integer> stack = new Stack<>();

        for (int i = 0; i < postfix.length(); i++) {
            char ch = postfix.charAt(i);

            // if number
            if (Character.isDigit(ch)) {
                stack.push(ch - '0'); // convert char to int
            } // if operator
            else {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                int result = 0;

                switch (ch) {
                    case '+':
                        result = operand1 + operand2;
                        break;
                    case '-':
                        result = operand1 - operand2;
                        break;
                    case '*':
                        result = operand1 * operand2;
                        break;
                    case '/':
                        result = operand1 / operand2;
                        break;
                }
                stack.push(result);
            }
        }
        return stack.pop();

    }
}

public class lab2 {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter an infix expression: ");
        String infix = input.nextLine();

        String postfix = Postfix.convert(infix);
        System.out.println("Postfix expression: " + postfix);
        int result = Postfix.evaluate(postfix);
        System.out.println("Result: " + result);
    }
}
