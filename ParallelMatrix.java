import java.util.concurrent.CountDownLatch;

public class ParallelMatrix {
    static final int N = 8; // розмір матриці (наприклад 8x8)
    static int[][] MA = new int[N][N];
    static int[][] MB = new int[N][N];
    static int[][] MC = new int[N][N];
    static int[][] MO = new int[N][N];

    static class Worker extends Thread {
        int startRow, endRow;
        CountDownLatch latch;

        Worker(int startRow, int endRow, CountDownLatch latch) {
            this.startRow = startRow;
            this.endRow = endRow;
            this.latch = latch;
        }

        @Override
        public void run() {
            for (int i = startRow; i < endRow; i++) {
                for (int j = 0; j < N; j++) {
                    int sum = 0;
                    for (int k = 0; k < N; k++) {
                        sum += MB[i][k] * MC[k][j];
                    }
                    MA[i][j] = sum - MO[i][j];
                }
            }
            latch.countDown();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // Ініціалізація матриць
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                MB[i][j] = 1;
                MC[i][j] = 2;
                MO[i][j] = 3;
            }
        }

        int numThreads = 4;
        int rowsPerThread = N / numThreads;
        CountDownLatch latch = new CountDownLatch(numThreads);

        // Створюємо та запускаємо потоки
        for (int t = 0; t < numThreads; t++) {
            int start = t * rowsPerThread;
            int end = (t == numThreads - 1) ? N : start + rowsPerThread;
            new Worker(start, end, latch).start();
        }

        // Очікуємо завершення
        latch.await();

        // Вивід результату
        System.out.println("Матриця MA = MB * MC - MO:");
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                System.out.print(MA[i][j] + "\t");
            }
            System.out.println();
        }
    }
}
