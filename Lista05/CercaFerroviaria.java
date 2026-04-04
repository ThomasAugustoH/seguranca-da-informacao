public class CercaFerroviaria {

    public String cifrar(String textoPuro, int qtTrilhos) {
        textoPuro = textoPuro.replace(" ", "");
        String[] trilhos = new String[qtTrilhos];
        int trilhoAtual = 0;
        boolean estaDescendo = true;

        for (int i = 0; i < trilhos.length; i++) {
            trilhos[i] = "";
        }
        
        for (int i = 0; i < textoPuro.length(); i++) {
            for (int j = 0; j < qtTrilhos; j++) {
                if (trilhoAtual == j) {
                    trilhos[j] += textoPuro.charAt(i);
                } else {
                    trilhos[j] += '.';
                }
            }

            if (estaDescendo) {
                if (trilhoAtual + 1 == qtTrilhos) {
                    trilhoAtual--;
                    estaDescendo = false;
                } else {
                    trilhoAtual++;
                }
            } else {
                if (trilhoAtual == 0) {
                    trilhoAtual ++;
                    estaDescendo = true;
                } else {
                    trilhoAtual--;
                }
            }
        }

        System.out.println("Trilho montado:");
        for (String trilho : trilhos) {
            System.out.println(trilho);
        }

        String textoCifrado = "";
        for (String string : trilhos) {
            for (int i = 0; i < string.length(); i++) {
                if (string.charAt(i) != '.') {
                    textoCifrado += string.charAt(i);
                }
            }
        }

        return textoCifrado;
    }

    public String decifrar(String textoCifrado, int qtTrilhos) {
        
        String[] trilhos = new String[qtTrilhos];
        int trilhoAtual = 0;
        boolean estaDescendo = true;

        for (int i = 0; i < trilhos.length; i++) {
            trilhos[i] = "";
        }
        
        for (int i = 0; i < textoCifrado.length(); i++) {
            for (int j = 0; j < qtTrilhos; j++) {
                if (trilhoAtual == j) {
                    trilhos[j] += '@';
                } else {
                    trilhos[j] += '.';
                }
            }

            if (estaDescendo) {
                if (trilhoAtual + 1 == qtTrilhos) {
                    trilhoAtual--;
                    estaDescendo = false;
                } else {
                    trilhoAtual++;
                }
            } else {
                if (trilhoAtual == 0) {
                    trilhoAtual ++;
                    estaDescendo = true;
                } else {
                    trilhoAtual--;
                }
            }
        }

        System.out.println("Trilho montado:");
        for (String trilho : trilhos) {
            System.out.println(trilho);
        }

        String[] trilhosDecifrados = new String[qtTrilhos];
        for (int i = 0; i < trilhosDecifrados.length; i++) {
            trilhosDecifrados[i] = "";
        }

        int index = 0;

        for (int i = 0; i < trilhos.length; i++) {
            for (int j = 0; j < textoCifrado.length(); j++) {
                if (trilhos[i].charAt(j) == '@') {
                    trilhosDecifrados[i] += textoCifrado.charAt(index);
                    index++;
                } else {
                    trilhosDecifrados[i] += '.';
                }
            }
        }

        System.out.println("Trilho decifrado:");
        for (String trilho : trilhosDecifrados) {
            System.out.println(trilho);
        }

        String textoDecifrado = "";
        trilhoAtual = 0;
        estaDescendo = true;
        for (int i = 0; i < textoCifrado.length(); i++) {
            for (int j = 0; j < qtTrilhos; j++) {
                if (trilhoAtual == j) {
                    textoDecifrado += trilhosDecifrados[j].charAt(i);
                }
            }

            if (estaDescendo) {
                if (trilhoAtual + 1 == qtTrilhos) {
                    trilhoAtual--;
                    estaDescendo = false;
                } else {
                    trilhoAtual++;
                }
            } else {
                if (trilhoAtual == 0) {
                    trilhoAtual ++;
                    estaDescendo = true;
                } else {
                    trilhoAtual--;
                }
            }
        }

        return textoDecifrado;
    }
}
