
import java.nio.file.Files;
import java.nio.file.Path;

public class App {

    private static byte[] chave = {65, 66, 67, 68, 69};
    private static String textoSimples;
    private static byte[] textoCifrado;
    private static String textoDecifrado;

    public static void main(String[] args) throws Exception {
        Blowfish blowfishCBC = new Blowfish(ModoOperacao.CBC);
        Blowfish blowfishECB = new Blowfish(ModoOperacao.ECB);
        Blowfish blowfishPCBC = new Blowfish(ModoOperacao.PCBC);
        Blowfish blowfishCTR = new Blowfish(ModoOperacao.CTR);

        // Caso 1
        System.out.println("----- CASO 1 -----");
        textoSimples = "FURB";
        textoCifrado = blowfishECB.cifrar(textoSimples, chave);
        System.out.println("Conteúdo do texto cifrado:");
        System.out.println(blowfishECB.textoEmBytes(textoCifrado));
        System.out.println("Tamanho do texto cifrado: " + textoCifrado.length);

        // Caso 2
        System.out.println("\n----- CASO 2 -----");
        textoSimples = "COMPUTADOR";
        textoCifrado = blowfishECB.cifrar(textoSimples, chave);
        System.out.println("Conteúdo do texto cifrado:");
        System.out.println(blowfishECB.textoEmBytes(textoCifrado));
        System.out.println("Tamanho do texto cifrado: " + textoCifrado.length);
        System.out.println("O conteúdo tem esse tamanho, pois a palavra COMPUTADOR tem mais de 8 caracteres e menos de 16.\n Foram gerados dois blocos, sendo que no último foi feito preenchimento (padding) até completá-lo.");

        // Caso 3
        System.out.println("\n----- CASO 3 -----");
        textoSimples = "SABONETE";
        textoCifrado = blowfishECB.cifrar(textoSimples, chave);
        System.out.println("Conteúdo do texto cifrado:");
        System.out.println(blowfishECB.textoEmBytes(textoCifrado));
        System.out.println("Tamanho do texto cifrado: " + textoCifrado.length);
        System.out.println("O conteúdo tem esse tamanho, pois o bloco anterior estava cheio.\n Neste caso é feito um bloco novo para adicionar o padding.");

        // Caso 4
        System.out.println("\n----- CASO 4 -----");
        byte[] bytesSimples = {8, 8, 8, 8, 8, 8, 8, 8};
        textoCifrado = blowfishECB.cifrar(bytesSimples, chave);
        System.out.println("Conteúdo do texto cifrado:");
        System.out.println(blowfishECB.textoEmBytes(textoCifrado));
        System.out.println("O padding anterior era composto de 8 bytes '8', semelhante ao texto cifrado por esse caso.\n Aqui é cifrado um bloco de 8 bytes '8', e adicionado outro padding de 8 bytes '8'.");

        // Caso 5
        System.out.println("\n----- CASO 5 -----");
        textoSimples = "SABONETESABONETESABONETE";
        textoCifrado = blowfishECB.cifrar(textoSimples, chave);
        System.out.println("Conteúdo do texto cifrado:");
        System.out.println(blowfishECB.textoEmBytes(textoCifrado));
        System.out.println("Tamanho do texto cifrado: " + textoCifrado.length);
        System.out.println("Como o texto simples é composto de 3 repetições da mesma palavra de 8 letras, a cifra ECB\n resulta num texto cifrado de 3 blocos idênticos de 8 bytes, adicionado a um padding de 8 bytes no final.");

        // Caso 6
        System.out.println("\n----- CASO 6 -----");
        textoSimples = "FURB";
        byte[] vetorInicializacao = {1, 1, 2, 2, 3, 3, 4, 4};
        textoCifrado = blowfishCBC.cifrar(textoSimples, chave, vetorInicializacao);
        System.out.println("Conteúdo do texto cifrado:");
        System.out.println(blowfishCBC.textoEmBytes(textoCifrado));
    
        // Caso 7
        System.out.println("\n----- CASO 7 -----");
        textoSimples = "SABONETESABONETESABONETE";
        textoCifrado = blowfishCBC.cifrar(textoSimples, chave, vetorInicializacao);
        System.out.println("Conteúdo do texto cifrado:");
        System.out.println(blowfishCBC.textoEmBytes(textoCifrado));
        System.out.println("Enquanto que no modo ECB o texto resultante é uma repetição dos 8 bytes em cada bloco,\n o modo CBC gera cifras diferentes para cada bloco criptografado.");

        // Caso 8
        System.out.println("\n----- CASO 8 -----");
        textoSimples = "SABONETESABONETESABONETE";
        byte[] vetorInicializacao2 = {10, 20, 30, 40, 50, 60, 70, 80};
        textoCifrado = blowfishCBC.cifrar(textoSimples, chave, vetorInicializacao2);
        System.out.println("Conteúdo do texto cifrado:");
        System.out.println(blowfishCBC.textoEmBytes(textoCifrado));
        System.out.println("Enquanto que no modo ECB o texto resultante é uma repetição dos 8 bytes em cada bloco, \no modo CBC gera cifras diferentes para cada bloco criptografado.");
        System.out.println("\nTexto decifrado com vetor de inicialização do caso 7:");
        System.out.println(blowfishCBC.decifrar(textoCifrado, chave, vetorInicializacao));
        System.out.println("Utilizando um outro vetor de inicialização, apenas o bloco inicial é comprometido. \nComo os outros blocos dependem apenas do bloco cifrado anterior e da chave, \neles podem ser decifrados sem o vetor de inicialização.");

        // Caso 9
        System.out.println("\n----- CASO 9 -----");
        textoSimples = "FURB";
        textoCifrado = blowfishECB.cifrar(textoSimples, chave);
        System.out.println("Texto decifrado com chave \"11111\":");
        byte[] chave2 = {1, 1, 1, 1, 1};
        textoDecifrado = blowfishECB.decifrar(textoCifrado, chave2);
        System.out.println("A exceção é causada pois não é possível descriptografar o texto\n com a chave incorreta, gerando um padding inválido.");

        // Caso 10
        System.out.println("\n----- CASO 10 -----");
        byte[] chave3 = "ABCDE".getBytes();
        byte[] arquivoSimples = Files.readAllBytes((Path.of("entrada.pdf")));
        byte[] arquivoCifrado = blowfishECB.cifrar(arquivoSimples, chave3);
        Files.write(Path.of("saida.bin"), arquivoCifrado);
        System.out.println("Tamanho do arquivo simples: " + arquivoSimples.length);
        System.out.println("Tamanho do arquivo cifrado: " + arquivoCifrado.length);

        // Caso 11
        System.out.println("\n----- CASO 11 -----");
        byte[] arquivoDecifrado = blowfishECB.decifrarEmBytes(arquivoCifrado, chave3);
        Files.write(Path.of("descriptografado.pdf"), arquivoDecifrado);
        System.out.println("Arquivo salvo.");

        // Caso 12
        System.out.println("\n----- CASO 12 -----");
        textoSimples = "FURB";
        textoCifrado = blowfishPCBC.cifrar(textoSimples, chave);
        System.out.println("Texto cifrado:");
        System.out.println(blowfishPCBC.textoEmBytes(textoCifrado));

        // Caso 13
        System.out.println("\n----- CASO 13 -----");
        textoSimples = "FURB";
        byte[] nonce = {0, 20, 10, 120, 0, 0, 0, 0};
        textoCifrado = blowfishCTR.cifrar(textoSimples, chave, nonce);
        textoDecifrado = blowfishCTR.decifrar(textoCifrado, chave, nonce);
        System.out.println("Texto simples:");
        System.out.println(textoDecifrado);
    }
}
