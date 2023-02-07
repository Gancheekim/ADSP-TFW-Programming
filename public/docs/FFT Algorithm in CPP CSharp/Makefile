CC=g++
LDFLAGS=-std=c++11 -O3 -lm
SOURCES=src/FFT.cpp 
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=fft

all: $(SOURCES) bin/$(EXECUTABLE)

bin/$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

%.o:  %.c  ${INCLUDES}
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf *.o bin/$(EXECUTABLE)
