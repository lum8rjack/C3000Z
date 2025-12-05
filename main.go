package main

import (
	"crypto/cipher"
	"crypto/des"
	"crypto/md5"
	"crypto/rand"
	"encoding/base64"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"strings"
)

// EVP_BytesToKey with optional salt (OpenSSL style)
func evpBytesToKey(password, salt []byte) (key, iv []byte) {
	var digest []byte
	var result []byte
	keyLen := 8 // DES key
	ivLen := 8  // DES block size
	for len(result) < keyLen+ivLen {
		h := md5.New()
		h.Write(digest)
		h.Write(password)
		if salt != nil {
			h.Write(salt)
		}
		digest = h.Sum(nil)
		result = append(result, digest...)
	}
	key = result[:keyLen]
	iv = result[keyLen : keyLen+ivLen]
	return
}

// Encrypt OpenSSL-compatible DES-CBC with salt and Base64
func encryptOpenSSLDES(plaintext, password []byte) (string, error) {
	// Generate random 8-byte salt
	salt := make([]byte, 8)
	if _, err := io.ReadFull(rand.Reader, salt); err != nil {
		return "", err
	}

	key, iv := evpBytesToKey(password, salt)

	block, err := des.NewCipher(key)
	if err != nil {
		return "", err
	}

	// PKCS5 padding
	blockSize := block.BlockSize()
	padLen := blockSize - len(plaintext)%blockSize
	padding := make([]byte, padLen)
	for i := range padding {
		padding[i] = byte(padLen)
	}
	plaintext = append(plaintext, padding...)

	ciphertext := make([]byte, len(plaintext))
	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(ciphertext, plaintext)

	// Prepend "Salted__" + salt
	out := append([]byte("Salted__"), salt...)
	out = append(out, ciphertext...)

	return base64.StdEncoding.EncodeToString(out), nil
}

// Decrypt OpenSSL-compatible DES-CBC with Base64
func decryptOpenSSLDES(ciphertextB64, password []byte) ([]byte, error) {
	data, err := base64.StdEncoding.DecodeString(string(ciphertextB64))
	if err != nil {
		return nil, err
	}

	if len(data) < 16 || string(data[:8]) != "Salted__" {
		return nil, errors.New("invalid OpenSSL salted format")
	}

	salt := data[8:16]
	ciphertext := data[16:]

	key, iv := evpBytesToKey(password, salt)
	block, err := des.NewCipher(key)
	if err != nil {
		return nil, err
	}

	if len(ciphertext)%block.BlockSize() != 0 {
		return nil, errors.New("ciphertext is not a multiple of block size")
	}

	plaintext := make([]byte, len(ciphertext))
	mode := cipher.NewCBCDecrypter(block, iv)
	mode.CryptBlocks(plaintext, ciphertext)

	// Remove PKCS5 padding
	padLen := int(plaintext[len(plaintext)-1])
	if padLen > 0 && padLen <= block.BlockSize() {
		plaintext = plaintext[:len(plaintext)-padLen]
	}

	return plaintext, nil
}

func main() {
	key := flag.String("key", "C1000Z_1234", "encryption key")
	data := flag.String("data", "", "data to encrypt/decrypt")
	mode := flag.String("mode", "decrypt", "encrypt or decrypt the data")
	flag.Parse()

	if *data == "" {
		flag.Usage()
		fmt.Println("\nYou must specify the data to encrypt/decrypt")
		os.Exit(0)
	}

	keyBytes := []byte(*key)
	dataBytes := []byte(*data)

	if strings.ToLower(*mode) == "decrypt" {
		decrypted, err := decryptOpenSSLDES(dataBytes, keyBytes)
		if err != nil {
			fmt.Printf("Error decrypting: %v\n", err)
		}
		fmt.Println("Decrypted:", string(decrypted))
	} else if strings.ToLower(*mode) == "encrypt" {
		ciphertext, err := encryptOpenSSLDES(dataBytes, keyBytes)
		if err != nil {
			fmt.Printf("Error encrypting: %v\n", err)
		}
		fmt.Println("Encrypted:", ciphertext)
	} else {
		flag.Usage()
		fmt.Printf("\nInvalide mode provided: %s\n", *mode)
		os.Exit(0)
	}
}
