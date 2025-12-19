import java.security.SecureRandom;

public class RandomGenerator {
    public static void main(String[] args) {
        //Создание генератора
        SecureRandom secureRandom = new SecureRandom();
        int len=128;
        StringBuilder binarySequence = new StringBuilder(len);

        for (int i = 0; i < len; i++) {
            int bit = secureRandom.nextInt(2);
            binarySequence.append(bit);
        }

        System.out.println("Generated Binary Sequence:");
        System.out.println(binarySequence.toString());
    }
}