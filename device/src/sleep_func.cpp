#include <Arduino.h>
#include "io_pins.h"
#include "esp_sleep.h"
#include "driver/rtc_io.h"
#include "soc/rtc_cntl_reg.h"
#include "soc/dport_reg.h"
#include "soc/i2s_reg.h"
#include "soc/sens_reg.h"
#include "soc/syscon_reg.h"

#define uS_TO_S_FACTOR 1000000ULL //1秒

/**
 * @brief 
 */
static void clearReg(){
    SET_PERI_REG_BITS(RTC_CNTL_TEST_MUX_REG, RTC_CNTL_DTEST_RTC, 0, RTC_CNTL_DTEST_RTC_S);
    CLEAR_PERI_REG_MASK(RTC_CNTL_TEST_MUX_REG, RTC_CNTL_ENT_RTC);
    CLEAR_PERI_REG_MASK(RTC_CNTL_CLK_CONF_REG, RTC_CNTL_CK8M_FORCE_PU);
}

/**
 * @brief n秒間DeepSleepする[割り込み許可]
 */
static void deepSleep(int n){
    // スリープの設定(SLOWメモリとインターセプトを許可する)
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_ON);
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_SLOW_MEM, ESP_PD_OPTION_ON);
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_FAST_MEM, ESP_PD_OPTION_OFF);
    esp_sleep_pd_config(ESP_PD_DOMAIN_XTAL, ESP_PD_OPTION_OFF);
    esp_sleep_pd_config(ESP_PD_DOMAIN_MAX, ESP_PD_OPTION_OFF);
    // GPIO2を割り込み信号として設定
    esp_sleep_enable_ext0_wakeup(GPIO_NUM_2, (int)1);
    // n秒分だけスリープする(最大値: 18446744073709551615)
    esp_sleep_enable_timer_wakeup(uint64_t(n * uS_TO_S_FACTOR));
    esp_deep_sleep_start();
}

/**
 * @brief 
 * 強制スリープモードでのSleep[割り込み非許可]
 */
static void forceDeepSleep(int n){
    clearReg();
    // スリープの設定(SLOWメモリとインターセプトを許可する)
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_OFF);
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_SLOW_MEM, ESP_PD_OPTION_ON);
    esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_FAST_MEM, ESP_PD_OPTION_OFF);
    esp_sleep_pd_config(ESP_PD_DOMAIN_XTAL, ESP_PD_OPTION_OFF);
    esp_sleep_pd_config(ESP_PD_DOMAIN_MAX, ESP_PD_OPTION_OFF);
    // n秒分だけスリープする(最大値: 18446744073709551615)
    esp_sleep_enable_timer_wakeup(uint64_t(n * uS_TO_S_FACTOR));
    esp_deep_sleep_start();
}