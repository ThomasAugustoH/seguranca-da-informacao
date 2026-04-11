import java.util.Scanner;

public class App {

    public static void main(String[] args) {

        Vegenere vegenere = new Vegenere();
        Scanner scanner = new Scanner(System.in);
        int opcao = 0;

        do {
            System.out.println("Escolha uma opção: ");
            System.out.println("1 - Cifrar texto");
            System.out.println("2 - Decifrar texto");
            System.out.println("3 - Sair do programa");

            String entrada = scanner.nextLine();
            if (!entrada.matches("[1-3]")) {
                System.out.println("Opção inválida!\n");
            } else {
                opcao = Integer.parseInt(entrada);
            }

            switch (opcao) {
                case 1:
                    System.out.println("\n----- CIFRAR TEXTO -----");
                    System.out.println("Forneça um texto para cifrar: ");
                    String textoPuro = scanner.nextLine();
                    System.out.println("Forneça uma chave: ");
                    String chave = scanner.nextLine();
                    String textoCifrado = vegenere.cifrar(textoPuro, chave);
                    System.out.println("Texto cifrado:\n" + textoCifrado);
                    System.out.println();
                    break;
            
                case 2:
                    System.out.println("\n----- DECIFRAR TEXTO -----");
                    System.out.println("Forneça um texto para decifrar: ");
                    textoCifrado = scanner.nextLine();
                    System.out.println("Forneça uma chave: ");
                    chave = scanner.nextLine();
                    String textoDecifrado = vegenere.decifrar(textoCifrado, chave);
                    System.out.println("Texto decifrado:\n" + textoDecifrado);
                    System.out.println();
                    break;
            }

        } while (opcao != 3);
        System.out.println("Saindo do programa...");
        scanner.close();
    }
}
