NAME := c3000z
BUILD := go build -ldflags "-s -w" -trimpath

default:
	@echo "Compiling"
	$(BUILD) -o $(NAME).bin

linux:
	@echo "Compiling for Linux x64"
	GOOS=linux GOARCH=amd64 $(BUILD) -o $(NAME)-Linux64.bin

arm:
	@echo "Compiling for Linux Arm64"
	GOOS=linux GOARCH=arm64 $(BUILD) -o $(NAME)-LinuxArm64.bin

windows:
	@echo "Compiling for Windows x64"
	GOOS=windows GOARCH=amd64 $(BUILD) -o $(NAME)-Windows64.exe

mac:
	@echo "Compiling for Mac"
	GOOS=darwin GOARCH=amd64 $(BUILD) -o $(NAME)-Mac.bin

m1:
	@echo "Compiling for Mac M1"
	GOOS=darwin GOARCH=arm64 $(BUILD) -o $(NAME)-MacM1.bin

