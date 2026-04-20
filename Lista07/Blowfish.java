import com.sun.jdi.InvalidTypeException;
import java.util.HexFormat;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class Blowfish {

    private Cipher cipher;
    private SecretKeySpec secretKeySpec;
    private ModoOperacao modo;

    public Blowfish(ModoOperacao modo) throws Exception {
        this.modo = modo;        
        if (modo == ModoOperacao.CTR) {
            cipher = Cipher.getInstance("Blowfish/CTR/NoPadding");
        } else {
            cipher = Cipher.getInstance("Blowfish/" + modo + "/PKCS5Padding");
        }
    }

    public byte[] cifrar(byte[] bytesSimples, byte[] chave) throws Exception {

        secretKeySpec = new SecretKeySpec(chave, "Blowfish");
        cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec);
        byte[] bytesCifrados = cipher.doFinal(bytesSimples);
        
        return bytesCifrados;
    }

    public byte[] cifrar(String textoSimples, byte[] chave) throws Exception {
        
        return cifrar(textoSimples.getBytes(), chave);
    }

    public byte[] cifrar(byte[] bytesSimples, byte[] chave, byte[] vetorInicializacao) throws Exception {
        if (modo != ModoOperacao.CBC && modo != ModoOperacao.CTR) {
            throw new InvalidTypeException();
        }

        secretKeySpec = new SecretKeySpec(chave, "Blowfish");
        IvParameterSpec ivParameter = new IvParameterSpec(vetorInicializacao);
        cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec, ivParameter);
        byte[] bytesCifrados = cipher.doFinal(bytesSimples);
        
        return bytesCifrados;
    }

    public byte[] cifrar(String textoSimples, byte[] chave, byte[] vetorInicializacao) throws Exception {
        
        return cifrar(textoSimples.getBytes(), chave, vetorInicializacao);
    }

    public byte[] decifrarEmBytes(byte[] bytesCifrados, byte[] chave) throws Exception {

        try {
        secretKeySpec = new SecretKeySpec(chave, "Blowfish");
        cipher.init(Cipher.DECRYPT_MODE, secretKeySpec);
        byte[] bytesDecifrados = cipher.doFinal(bytesCifrados);

        return bytesDecifrados;
        
        } catch (Exception e){
            
            System.out.println("Erro: " + e.getMessage());
            return null;
        }
    }

    public String decifrar(byte[] bytesCifrados, byte[] chave) throws Exception {

        try {
            return new String(decifrarEmBytes(bytesCifrados, chave));
        } catch (Exception e){
            System.out.println("Erro: " + e.getMessage());
            return null;
        }
    }

    public byte[] decifrarEmBytes(byte[] bytesCifrados, byte[] chave, byte[] vetorInicializacao) throws Exception {
        if (modo != ModoOperacao.CBC && modo != ModoOperacao.CTR) {
            throw new InvalidTypeException();
        }

        try {
        secretKeySpec = new SecretKeySpec(chave, "Blowfish");
        IvParameterSpec ivParameter = new IvParameterSpec(vetorInicializacao);
        cipher.init(Cipher.DECRYPT_MODE, secretKeySpec, ivParameter);
        byte[] bytesDecifrados = cipher.doFinal(bytesCifrados);
        
        return bytesDecifrados;
        } catch (Exception e){
            
            System.out.println("Exceção: " + e.getMessage());
            return null;
        }
    }

    public String decifrar(byte[] bytesCifrados, byte[] chave, byte[] vetorInicializacao) throws Exception {
        
        try {
        return new String(decifrarEmBytes(bytesCifrados, chave, vetorInicializacao));
        } catch (Exception e){
            System.out.println("Erro: " + e.getMessage());
            return null;
        }
    }

    public String textoEmBytes(byte[] bytesCifrados) {

        String textoFinal = "";

        int contador = 0;
        for (byte b : bytesCifrados) {
            if (contador == 8) {
                contador = 0;
                textoFinal += "\n";
            }
            textoFinal += HexFormat.of().toHexDigits(b).toUpperCase() + " ";
            contador++;
        }

        return textoFinal;
    }
}
