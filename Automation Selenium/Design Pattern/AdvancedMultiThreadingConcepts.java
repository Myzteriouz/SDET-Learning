import java.util.concurrent.*;
import java.util.concurrent.locks.ReentrantLock;

/**
 * This class demonstrates advanced multithreading concepts in Java, including
 * visibility (volatile), thread isolation (ThreadLocal), thread pools, 
 * synchronization aids, and advanced locking mechanisms.
 */
public class AdvancedMultiThreadingConcepts {

    /* =========================================================================
     * 1. THE 'volatile' KEYWORD
     * =========================================================================
     * 
     * Concept: 'volatile' is used to mark a Java variable as being stored in 
     * main memory. Without it, threads might cache the variable's value locally 
     * for performance. If one thread updates the variable, the other thread might 
     * not see the update immediately (or ever) because it's reading from its cache.
     * 
     * Usage: It guarantees "visibility" of changes across threads. It does NOT 
     * guarantee "atomicity" (like thread-safe incrementing).
     */
    private static volatile boolean shutdownRequested = false;

    /* =========================================================================
     * 2. ThreadLocal
     * =========================================================================
     * 
     * Concept: ThreadLocal provides variables that can only be read and written 
     * by the same thread. Even if multiple threads execute the same code, they 
     * will not see each other's ThreadLocal variables.
     * 
     * Usage: Extremely useful in frameworks (like Selenium WebDrivers or Spring 
     * Security context) to maintain session/state without passing it down the 
     * method chain.
     */
    private static ThreadLocal<String> userContext = ThreadLocal.withInitial(() -> "Guest");

    /* =========================================================================
     * 3. ReentrantLock
     * =========================================================================
     * 
     * Concept: An advanced alternative to the traditional 'synchronized' keyword.
     * It allows fairness (first-in-first-out thread execution), interruptible 
     * lock waits, and the ability to try acquiring a lock without blocking forever.
     */
    private static ReentrantLock customLock = new ReentrantLock();

    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("Starting Advanced Multithreading Concepts Demonstration...\n");

        demonstrateVolatile();
        demonstrateThreadLocal();
        demonstrateExecutorServiceAndLatch();
    }

    /**
     * Demonstrates how 'volatile' ensures a thread sees updates made by another.
     */
    private static void demonstrateVolatile() throws InterruptedException {
        System.out.println("--- 1. Demonstrating 'volatile' ---");
        
        Thread backgroundWorker = new Thread(() -> {
            long count = 0;
            // If shutdownRequested was NOT volatile, this loop might run infinitely 
            // because the thread might never see the change made by the main thread.
            while (!shutdownRequested) {
                count++;
            }
            System.out.println("Background worker noticed shutdown request. Stopped at: " + count);
        });

        backgroundWorker.start();
        
        Thread.sleep(100); // Let the background worker run for a brief moment
        System.out.println("Main thread requesting shutdown...");
        shutdownRequested = true; // Updates the volatile variable in main memory
        
        backgroundWorker.join(); // Wait for the worker to finish
        System.out.println();
    }

    /**
     * Demonstrates how ThreadLocal isolates data per thread.
     */
    private static void demonstrateThreadLocal() throws InterruptedException {
        System.out.println("--- 2. Demonstrating 'ThreadLocal' ---");

        Runnable task = () -> {
            String threadName = Thread.currentThread().getName();
            System.out.println(threadName + " initial context: " + userContext.get());
            
            // Thread modifies its own isolated copy of the variable
            userContext.set("User_Logged_In_via_" + threadName);
            
            System.out.println(threadName + " modified context: " + userContext.get());
            
            // Always clean up ThreadLocal variables to prevent memory leaks in thread pools!
            userContext.remove();
        };

        Thread t1 = new Thread(task, "Thread-1");
        Thread t2 = new Thread(task, "Thread-2");

        t1.start();
        t2.start();

        t1.join();
        t2.join();
        System.out.println();
    }

    /**
     * Demonstrates Thread Pools (ExecutorService) and CountDownLatch.
     */
    private static void demonstrateExecutorServiceAndLatch() throws InterruptedException {
        System.out.println("--- 3. Demonstrating ExecutorService & CountDownLatch ---");
        
        // CountDownLatch allows one or more threads to wait until a set of operations 
        // being performed in other threads completes.
        int numberOfTasks = 3;
        CountDownLatch latch = new CountDownLatch(numberOfTasks);
        
        // ExecutorService manages a pool of worker threads, avoiding the overhead 
        // of manually creating new Thread() objects every time.
        ExecutorService executor = Executors.newFixedThreadPool(2); // Pool of 2 threads

        for (int i = 1; i <= numberOfTasks; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println(Thread.currentThread().getName() + " is executing Task " + taskId);
                latch.countDown(); // Decrement the latch count
            });
        }

        latch.await(); // Main thread waits here until latch count reaches 0
        System.out.println("All tasks completed. Main thread proceeding.");
        executor.shutdown(); // Always shut down your executor service!
    }
}