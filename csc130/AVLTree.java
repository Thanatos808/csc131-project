
import java.util.*;
import java.io.*;

public class AVLTree {

    // Node structure for AVL Tree
    class Node {

        int key;
        int height;
        Node left, right;

        Node(int key) {
            this.key = key;
            this.height = 0;
            left = right = null;
        }
    }

    int height(Node n) {
        return (n == null) ? -1 : n.height;
    }

    int max(int a, int b) {
        return (a > b) ? a : b;
    }

    int getBalance(Node n) {
        if (n == null) {
            return 0;
        }
        return height(n.left) - height(n.right);
    }

    // LEFT ROTATION
    Node leftRotate(Node x) {
        Node y = x.right;
        Node T2 = y.left;

        y.left = x;
        x.right = T2;

        x.height = max(height(x.left), height(x.right)) + 1;
        y.height = max(height(y.left), height(y.right)) + 1;

        return y;
    }

    // RIGHT ROTATION
    Node rightRotate(Node x) {
        Node y = x.left;
        Node T2 = y.right;

        y.right = x;
        x.left = T2;

        x.height = max(height(x.left), height(x.right)) + 1;
        y.height = max(height(y.left), height(y.right)) + 1;

        return y;
    }

    // REBALANCE FUNCTION
    Node rebalance(Node n) {

        n.height = max(height(n.left), height(n.right)) + 1;
        int balance = getBalance(n);

        // LEFT HEAVY
        if (balance > 1) {
            if (getBalance(n.left) >= 0) {
                return rightRotate(n);
            } else {
                n.left = leftRotate(n.left);
                return rightRotate(n);
            }
        }

        // RIGHT HEAVY
        if (balance < -1) {
            if (getBalance(n.right) <= 0) {
                return leftRotate(n);
            } else {
                n.right = rightRotate(n.right);
                return leftRotate(n);
            }
        }

        return n;
    }

    // INSERT FUNCTION
    Node insert(Node node, int key) {

        if (node == null) {
            return new Node(key);
        }

        if (key < node.key) {
            node.left = insert(node.left, key);
        } else {
            node.right = insert(node.right, key);
        }

        return rebalance(node);
    }

    // LEVEL ORDER PRINT (BFS using queue)
    void printLevel(Node root, PrintWriter out) {

        if (root == null) {
            return;
        }

        LinkedList<Node> q = new LinkedList<Node>();

        int currentLevel = 1;
        int nextLevel = 0;

        q.add(root);

        while (currentLevel != 0) {

            Node curr = q.poll();

            out.print(curr.key
                    + " (h=" + curr.height
                    + ", bf=" + getBalance(curr) + ") ");

            currentLevel--;

            if (curr.left != null) {
                q.add(curr.left);
                nextLevel++;
            }

            if (curr.right != null) {
                q.add(curr.right);
                nextLevel++;
            }

            if (currentLevel == 0) {
                out.println();
                currentLevel = nextLevel;
                nextLevel = 0;
            }
        }
    }

    public static void main(String[] args) throws Exception {

        Scanner in = new Scanner(new File("input.txt"));
        PrintWriter out = new PrintWriter("output.txt");

        AVLTree tree = new AVLTree();
        Node root = null;

        while (in.hasNextInt()) {
            root = tree.insert(root, in.nextInt());
        }

        tree.printLevel(root, out);

        in.close();
        out.close();
    }
}
