public enum ModoOperacao {
    ECB("ECB"),
    CBC("CBC"),
    PCBC("PCBC"),
    CTR("CTR");

    private final String valor;

    private ModoOperacao(String modo) {
        this.valor = modo;
    }

    public String getValor() {
        return valor;
    }
}
