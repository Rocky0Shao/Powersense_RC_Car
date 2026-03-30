# STM32F446RE NUCLEO - Hardware Component Map & Wiring

## Board Information

| Parameter | Value |
|-----------|-------|
| **MCU** | STM32F446RETx |
| **Board** | NUCLEO-F446RE |
| **Package** | LQFP64 |
| **Core Clock** | 84 MHz |
| **APB1 Clock** | 42 MHz |
| **APB2 Clock** | 84 MHz |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         NUCLEO-F446RE BOARD                                 │
│                                                                             │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                  │
│   │  ENCODER 1  │     │  ENCODER 2  │     │   I2C BUS   │                  │
│   │   (Left)    │     │   (Right)   │     │  (Sensors)  │                  │
│   │  TIM1 CH1/2 │     │  TIM2 CH1/2 │     │    I2C1     │                  │
│   │  PA8 / PA9  │     │  PA0 / PA1  │     │  PB8 / PB9  │                  │
│   └─────────────┘     └─────────────┘     └─────────────┘                  │
│                                                                             │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                  │
│   │   USART2    │     │  USER LED   │     │ USER BUTTON │                  │
│   │  (ST-Link)  │     │    LD2      │     │     B1      │                  │
│   │  PA2 / PA3  │     │    PA5      │     │    PC13     │                  │
│   └─────────────┘     └─────────────┘     └─────────────┘                  │
│                                                                             │
│   ┌──────────────────────────────────────┐                                 │
│   │           SWD DEBUG (ST-Link)        │                                 │
│   │   SWDIO: PA13  |  SWCLK: PA14  |  SWO: PB3                             │
│   └──────────────────────────────────────┘                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Pin Mapping Summary

### GPIO Overview

| Pin | Port | Function | Alternate Function | Description |
|-----|------|----------|-------------------|-------------|
| PA0 | GPIOA | TIM2_CH1 | AF1 | Encoder 2 Channel A (Right) |
| PA1 | GPIOA | TIM2_CH2 | AF1 | Encoder 2 Channel B (Right) |
| PA2 | GPIOA | USART2_TX | AF7 | Serial TX (ST-Link VCP) |
| PA3 | GPIOA | USART2_RX | AF7 | Serial RX (ST-Link VCP) |
| PA5 | GPIOA | GPIO_Output | — | LD2 Green LED |
| PA8 | GPIOA | TIM1_CH1 | AF1 | Encoder 1 Channel A (Left) |
| PA9 | GPIOA | TIM1_CH2 | AF1 | Encoder 1 Channel B (Left) |
| PA13 | GPIOA | SWDIO | — | Debug TMS |
| PA14 | GPIOA | SWCLK | — | Debug TCK |
| PB3 | GPIOB | SWO | — | Debug Trace Output |
| PB8 | GPIOB | I2C1_SCL | AF4 | I2C Clock |
| PB9 | GPIOB | I2C1_SDA | AF4 | I2C Data |
| PC13 | GPIOC | GPIO_EXTI | — | B1 Blue Push Button |
| PC14 | GPIOC | OSC32_IN | — | LSE Crystal Input |
| PC15 | GPIOC | OSC32_OUT | — | LSE Crystal Output |
| PH0 | GPIOH | OSC_IN | — | HSE Crystal Input |
| PH1 | GPIOH | OSC_OUT | — | HSE Crystal Output |

---

## Quadrature Encoder Interface

### Encoder 1 - Left Motor (TIM1)

```
        Encoder (Left Motor)
       ┌──────────────────┐
       │                  │
 CH_A ─┤──────────────────┼──► PA8 (TIM1_CH1)
       │                  │
 CH_B ─┤──────────────────┼──► PA9 (TIM1_CH2)
       │                  │
 VCC  ─┤──────────────────┼──► 3.3V or 5V
       │                  │
 GND  ─┤──────────────────┼──► GND
       └──────────────────┘
```

| Parameter | Value |
|-----------|-------|
| Timer | TIM1 |
| Mode | Encoder Interface (TI1 & TI2) |
| Channel A Pin | **PA8** (TIM1_CH1) |
| Channel B Pin | **PA9** (TIM1_CH2) |
| Input Filter | 5 (noise filtering) |
| Pull-up | Internal (GPIO_PULLUP) |
| Counter Period | 2399 (0-2399 = 2400 counts/rev) |
| Prescaler | 0 (no division) |

### Encoder 2 - Right Motor (TIM2)

```
        Encoder (Right Motor)
       ┌──────────────────┐
       │                  │
 CH_A ─┤──────────────────┼──► PA0 (TIM2_CH1)
       │                  │
 CH_B ─┤──────────────────┼──► PA1 (TIM2_CH2)
       │                  │
 VCC  ─┤──────────────────┼──► 3.3V or 5V
       │                  │
 GND  ─┤──────────────────┼──► GND
       └──────────────────┘
```

| Parameter | Value |
|-----------|-------|
| Timer | TIM2 |
| Mode | Encoder Interface (TI1 & TI2) |
| Channel A Pin | **PA0** (TIM2_CH1) |
| Channel B Pin | **PA1** (TIM2_CH2) |
| Input Filter | 5 (noise filtering) |
| Pull-up | Internal (GPIO_PULLUP) |
| Counter Period | 2399 (0-2399 = 2400 counts/rev) |
| Prescaler | 0 (no division) |

---

## I2C Bus (I2C1)

```
        I2C Device (e.g., IMU, Sensor)
       ┌──────────────────┐
       │                  │
 SCL  ─┤──────────────────┼──► PB8 (I2C1_SCL)
       │                  │
 SDA  ─┤──────────────────┼──► PB9 (I2C1_SDA)
       │                  │
 VCC  ─┤──────────────────┼──► 3.3V
       │                  │
 GND  ─┤──────────────────┼──► GND
       └──────────────────┘

Note: External pull-up resistors (4.7kΩ) recommended on SDA/SCL lines
```

| Parameter | Value |
|-----------|-------|
| Peripheral | I2C1 |
| SCL Pin | **PB8** |
| SDA Pin | **PB9** |
| Clock Speed | 100 kHz (Standard Mode) |
| Addressing | 7-bit |
| Duty Cycle | 2:1 |
| GPIO Mode | Open-Drain, AF4 |

---

## USART2 (Virtual COM Port via ST-Link)

```
       ST-Link USB ◄──────────────────► PC
            │
            │  Virtual COM Port
            │
       ┌────┴────┐
       │ ST-Link │
       └────┬────┘
            │
    TX ─────┼──► PA2 (USART2_TX)
            │
    RX ◄────┼─── PA3 (USART2_RX)
            │
       STM32F446RE
```

| Parameter | Value |
|-----------|-------|
| Peripheral | USART2 |
| TX Pin | **PA2** |
| RX Pin | **PA3** |
| Baud Rate | 115200 |
| Word Length | 8 bits |
| Stop Bits | 1 |
| Parity | None |
| Flow Control | None |
| Oversampling | 16x |

---

## GPIO (LED & Button)

### LD2 - Green User LED

```
       PA5 ────────┬──────► LED ────► GND
                   │
              (Active High)
```

| Parameter | Value |
|-----------|-------|
| Pin | **PA5** |
| Port | GPIOA |
| Mode | Push-Pull Output |
| Active | High (LED ON when pin HIGH) |

### B1 - Blue User Button

```
       PC13 ◄──────┬────── Button ────── GND
                   │
           (Active Low, EXTI Falling Edge)
```

| Parameter | Value |
|-----------|-------|
| Pin | **PC13** |
| Port | GPIOC |
| Mode | External Interrupt (EXTI13) |
| Trigger | Falling Edge |
| Active | Low (pressed = LOW) |

---

## Complete Wiring Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           STM32F446RE NUCLEO                                │
│                                                                             │
│  MORPHO CONNECTOR (CN7/CN10)              ARDUINO CONNECTOR (CN5/CN6/CN8/CN9)
│  ════════════════════════                 ══════════════════════════════════│
│                                                                             │
│  ┌─────────── ENCODER LEFT (TIM1) ───────────┐                             │
│  │  PA8 (D7)  ◄─────────────────── Encoder A │                             │
│  │  PA9 (D8)  ◄─────────────────── Encoder B │                             │
│  │  3.3V      ─────────────────────► VCC     │                             │
│  │  GND       ─────────────────────► GND     │                             │
│  └───────────────────────────────────────────┘                             │
│                                                                             │
│  ┌─────────── ENCODER RIGHT (TIM2) ──────────┐                             │
│  │  PA0 (A0)  ◄─────────────────── Encoder A │                             │
│  │  PA1 (A1)  ◄─────────────────── Encoder B │                             │
│  │  3.3V      ─────────────────────► VCC     │                             │
│  │  GND       ─────────────────────► GND     │                             │
│  └───────────────────────────────────────────┘                             │
│                                                                             │
│  ┌─────────── I2C SENSOR (I2C1) ─────────────┐                             │
│  │  PB8 (D15) ◄────────────────────► SCL     │  ┌──► 4.7kΩ ──► 3.3V       │
│  │  PB9 (D14) ◄────────────────────► SDA     │  └──► 4.7kΩ ──► 3.3V       │
│  │  3.3V      ─────────────────────► VCC     │     (External Pull-ups)     │
│  │  GND       ─────────────────────► GND     │                             │
│  └───────────────────────────────────────────┘                             │
│                                                                             │
│  ┌─────────── USART2 (ST-Link VCP) ──────────┐                             │
│  │  PA2 (D1)  ────────────────────► TX       │                             │
│  │  PA3 (D0)  ◄──────────────────── RX       │  (Connected to ST-Link)     │
│  └───────────────────────────────────────────┘                             │
│                                                                             │
│  ┌─────────── ON-BOARD PERIPHERALS ──────────┐                             │
│  │  PA5       ────────────────────► LD2 (Green LED)                        │
│  │  PC13      ◄──────────────────── B1 (Blue Button)                       │
│  └───────────────────────────────────────────┘                             │
│                                                                             │
│  ┌─────────── DEBUG (SWD) ───────────────────┐                             │
│  │  PA13      ◄──────────────────── SWDIO    │                             │
│  │  PA14      ◄──────────────────── SWCLK    │  (Connected to ST-Link)     │
│  │  PB3       ────────────────────► SWO      │                             │
│  └───────────────────────────────────────────┘                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Arduino Header Pin Mapping

| Arduino Pin | STM32 Pin | Function in Project |
|-------------|-----------|---------------------|
| A0 | PA0 | Encoder 2 CH_A (TIM2_CH1) |
| A1 | PA1 | Encoder 2 CH_B (TIM2_CH2) |
| D0 | PA3 | USART2_RX |
| D1 | PA2 | USART2_TX |
| D7 | PA8 | Encoder 1 CH_A (TIM1_CH1) |
| D8 | PA9 | Encoder 1 CH_B (TIM1_CH2) |
| D14 | PB9 | I2C1_SDA |
| D15 | PB8 | I2C1_SCL |

---

## Clock Configuration

```
┌──────────────────────────────────────────────────────────────┐
│                    CLOCK TREE                                │
│                                                              │
│   HSI (16 MHz) ──► PLL ──► SYSCLK (84 MHz)                  │
│                       │                                      │
│                       ├──► AHB (84 MHz)                     │
│                       │       │                              │
│                       │       ├──► APB1 (42 MHz) ──► TIM2   │
│                       │       │                    ──► I2C1  │
│                       │       │                    ──► USART2│
│                       │       │                              │
│                       │       └──► APB2 (84 MHz) ──► TIM1   │
│                       │                                      │
│   LSE (32.768 kHz) ──► RTC                                  │
└──────────────────────────────────────────────────────────────┘
```

| Clock Domain | Frequency | Peripherals |
|--------------|-----------|-------------|
| SYSCLK | 84 MHz | Core |
| AHB | 84 MHz | DMA, GPIO |
| APB1 | 42 MHz | TIM2, I2C1, USART2 |
| APB1 Timer | 84 MHz | TIM2 counter |
| APB2 | 84 MHz | TIM1 |
| APB2 Timer | 84 MHz | TIM1 counter |

---

## Quick Reference Card

```
╔═══════════════════════════════════════════════════════════════════╗
║              STM32F446RE NUCLEO - PIN QUICK REFERENCE             ║
╠═══════════════════════════════════════════════════════════════════╣
║ ENCODER 1 (LEFT) - TIM1                                           ║
║   PA8 (D7)  ──► Channel A                                        ║
║   PA9 (D8)  ──► Channel B                                        ║
║   Period: 2400 counts | Filter: 5 | Pull-up: Enabled             ║
╠═══════════════════════════════════════════════════════════════════╣
║ ENCODER 2 (RIGHT) - TIM2                                          ║
║   PA0 (A0)  ──► Channel A                                        ║
║   PA1 (A1)  ──► Channel B                                        ║
║   Period: 2400 counts | Filter: 5 | Pull-up: Enabled             ║
╠═══════════════════════════════════════════════════════════════════╣
║ I2C1 (100 kHz Standard Mode)                                      ║
║   PB8 (D15) ──► SCL                                              ║
║   PB9 (D14) ──► SDA                                              ║
╠═══════════════════════════════════════════════════════════════════╣
║ USART2 (115200 baud, 8N1)                                         ║
║   PA2 (D1)  ──► TX                                               ║
║   PA3 (D0)  ──► RX                                               ║
╠═══════════════════════════════════════════════════════════════════╣
║ GPIO                                                              ║
║   PA5       ──► LD2 Green LED (Active High)                      ║
║   PC13      ──► B1 Blue Button (Active Low, EXTI)                ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## Notes

1. **Encoder Resolution**: Both encoders use TIM_ENCODERMODE_TI12, counting on both edges of both channels (4x decoding). With period=2399, counter wraps at 2400.

2. **I2C Pull-ups**: The I2C pins are configured without internal pull-ups (GPIO_NOPULL). External 4.7kΩ pull-up resistors to 3.3V are recommended.

3. **USART2 via ST-Link**: USART2 is routed through the on-board ST-Link debugger, providing a virtual COM port over USB.

4. **Input Filtering**: Encoder inputs use filter value 5 for noise rejection on the quadrature signals.

5. **Code reads encoders**: In `main.c`, the encoder counts are read via `TIM1->CNT` (enL) and `TIM2->CNT` (enR).
