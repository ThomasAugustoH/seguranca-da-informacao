public class Transposicao{

    public String cifrar(String textoPuro, int qtColunas) {
        textoPuro = textoPuro.replace(" ", "");
        int qtLinhas = (int) Math.ceil(textoPuro.length() / (float) qtColunas);

        int linha = 0;
        int coluna = 0;
        String textoCifrado = "";

        for (int i = 0; i < qtLinhas * qtColunas; i++) {
            int index = linha * qtColunas + coluna;
            if (textoPuro.length() > index) {
                textoCifrado += textoPuro.charAt(index);
            } else {
                textoCifrado += 'X';
            }

            linha++;
            if (linha >= qtLinhas) {
                linha = 0;
                coluna++;
            }
        }

        return textoCifrado;
    }

    public String decifrar(String textoCifrado, int qtColunas) {

        int qtLinhas = textoCifrado.length() / qtColunas;

        int linha = 0;
        int coluna = 0;
        String textoPuro = "";

        for (int i = 0; i < textoCifrado.length(); i++) {
            int index = coluna * qtLinhas + linha;

            textoPuro += textoCifrado.charAt(index);
            coluna++;
            if (coluna >= qtColunas) {
                coluna = 0;
                linha++;
            }
        }

        return textoPuro;
    }
}
