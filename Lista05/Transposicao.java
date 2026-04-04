public class Transposicao{

    public String cifrar(String textoPuro, int colunas) {
        textoPuro = textoPuro.replace(" ", "");
        
        char[][] matrizCifrada = gerarMatrizCifrada(textoPuro, colunas);
        int qtLinhas = (int) Math.ceil(textoPuro.length() / (float) colunas);

        String textoCifrado = "";

        for (int i = 0; i < colunas; i++) {
            for (int j = 0; j < qtLinhas; j++) {
                textoCifrado += matrizCifrada[j][i];
            }
        }

        return textoCifrado;
    }

    public String decifrar(String textoCifrado, int colunas) {

        int qtLinhas = textoCifrado.length() / colunas;

        int linha = 0;
        int coluna = 0;
        String textoPuro = "";

        for (int i = 0; i < textoCifrado.length(); i++) {

            textoPuro += textoCifrado.charAt(coluna * qtLinhas + linha);
            coluna++;
            if (coluna >= colunas) {
                coluna = 0;
                linha++;
            }
        }

        return textoPuro;
    }

    private char[][] gerarMatrizCifrada(String textoPuro, int colunas){
        int qtLinhas = (int) Math.ceil(textoPuro.length() / (float) colunas);
        char[][] matrizCifrada = new char[qtLinhas][colunas];
        int index = 0;

        for (int i = 0; i < qtLinhas; i++) {
            for (int j = 0; j < colunas; j++) {
                if (textoPuro.length() > index) {
                    matrizCifrada[i][j] = textoPuro.charAt(index);
                } else {
                    matrizCifrada[i][j] = 'X';
                }
                index++;
            }
        }

        return matrizCifrada;
    }
}
