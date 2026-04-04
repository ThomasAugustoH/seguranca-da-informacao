public class App {

    public static void main(String[] args) {
        System.out.println("------- TRANSPOSIÇÃO GEOMÉRICA COLUNAR -------");
        Transposicao transposicao = new Transposicao();
        String textoPuro = "VAMOS ATACAR O SUL NO FINAL DESTA SEMANA";
        int parametroColunas = 7;
        System.out.println("Entrada: " + textoPuro);

        String textoCifrado = transposicao.cifrar(textoPuro, parametroColunas);
        System.out.println("Texto cifrado: " + textoCifrado);

        String textoDecifrado = transposicao.decifrar(textoCifrado, parametroColunas);
        System.out.println("Texto decifrado: " + textoDecifrado);

        System.out.println("\n------- CERCA FERROVIÁRIA -------");
        CercaFerroviaria cercaFerroviaria = new CercaFerroviaria();
        textoPuro = "VAMOS INVADIR O SUL AMANHA";
        int parametroTrilhos = 3;
        System.out.println("Entrada: " + textoPuro);

        textoCifrado = cercaFerroviaria.cifrar(textoPuro, parametroTrilhos);
        System.out.println("Texto cifrado: " + textoCifrado);

        textoDecifrado = cercaFerroviaria.decifrar(textoCifrado, parametroTrilhos);
        System.out.println("Texto decifrado: " + textoDecifrado);

    }
}
