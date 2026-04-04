public class App {

    public static void main(String[] args) {
        Transposicao transposicao = new Transposicao();

        String textoPuro = "VAMOS ATACAR O SUL NO FINAL DESTA SEMANA";

        String textoCifrado = transposicao.cifrar(textoPuro, 7);
        System.out.println(textoCifrado);

        String textoDecifrado = transposicao.decifrar(textoCifrado, 7);
        System.out.println(textoDecifrado);
    }
}
