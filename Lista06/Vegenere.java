public class Vegenere {

    public String cifrar(String textoPuro, String chave){
        textoPuro = textoPuro.toUpperCase();
        chave = chave.toUpperCase();
        String textoCifrado = "";
        int c = 0;
    
        for (int i = 0; i < textoPuro.length(); i++) {
            if ((int) textoPuro.charAt(i) >= 65 && (int) textoPuro.charAt(i) <= 90) {
                int letraAntiga = ((int) textoPuro.charAt(i)) - 65;
                int letraChave = ((int) chave.charAt(c)) - 65;
                int novaLetra = (letraAntiga + letraChave) % 26;

                c += 1;
                c = c % chave.length();
                textoCifrado += (char) (novaLetra + 65);
            } else {
                textoCifrado += textoPuro.charAt(i);
            }

        }

        return textoCifrado;
    }

    public String decifrar(String textoCifrado, String chave) {
        chave = chave.toUpperCase();
        String textoPuro = "";
        int c = 0;
    
        for (int i = 0; i < textoCifrado.length(); i++) {
            if ((int) textoCifrado.charAt(i) >= 65 && (int) textoCifrado.charAt(i) <= 90) {
                int letraAntiga = ((int) textoCifrado.charAt(i)) - 65;
                int letraChave = ((int) chave.charAt(c)) - 65;
                int novaLetra = (26 + letraAntiga - letraChave) % 26;

                c += 1;
                c = c % chave.length();
                textoPuro += (char) (novaLetra + 65);
            } else {
                textoPuro += textoCifrado.charAt(i);
            }
        }


        return textoPuro;
    }
}
