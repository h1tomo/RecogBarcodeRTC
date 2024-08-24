#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file RecogBarcodeRTC.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

# Import ZBar packages
import cv2
from pyzbar import pyzbar
import numpy as np

timer = 0


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
recogbarcodertc_spec = ["implementation_id", "RecogBarcodeRTC", 
         "type_name",         "RecogBarcodeRTC", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "Hosokawa", 
         "category",          "ImageProcessiong", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class RecogBarcodeRTC
# @brief ModuleDescription
# 
# 
# </rtc-template>


def detect_and_draw_barcodes(frame):
        global productID 
        productID = 404
    # フレームからバーコードを検出
        barcodes = pyzbar.decode(frame)
    
        for barcode in barcodes:
            # バーコードの頂点座標を取得
      #      x, y, w, h = barcode.rect
      #      print(str(x) + " , " + str(y) + " , " + str(w) + " , " +str(h))
      #      # バーコードを矩形で囲う
      #      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
      #      # 頂点を描画
      #      cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)
      #      cv2.circle(frame, (x + w, y), 4, (0, 255, 0), -1)
      #      cv2.circle(frame, (x, y + h), 4, (255, 0, 0), -1)
      #      cv2.circle(frame, (x + w, y + h), 4, (255, 255, 0), -1)
        
      #      # バーコードのデータを表示
            barcode_data = barcode.data.decode("utf-8")  # utf-8:文字コード
            bar_num = int(barcode_data)
            least_three = bar_num % 1000
            
            productID = least_three // 10;  #バーコードから下２，３桁目の値を取得
            print("Detected productID:", productID)

      #      barcode_type = barcode.type
      #      # 画面上に表示するテキストの整形
      #      text = f"{barcode_type}: {barcode_data}"
		    ## テキストを描画
      #      cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame, productID

class RecogBarcodeRTC(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_image_in = OpenRTM_aist.instantiateDataType(RTC.CameraImage)
        """
        """
        self._image_inIn = OpenRTM_aist.InPort("image_in", self._d_image_in)
        self._d_id_out = OpenRTM_aist.instantiateDataType(RTC.TimedLong)
        """
        """
        self._id_outOut = OpenRTM_aist.OutPort("id_out", self._d_id_out)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
		
        # Set InPort buffers
        self.addInPort("image_in",self._image_inIn)
		
        # Set OutPort buffers
        self.addOutPort("id_out",self._id_outOut)
		
        # Set service provider to Ports
		
        # Set service consumers to Ports
		
        # Set CORBA Service Ports
		
        return RTC.RTC_OK
	
    ###
    ## 
    ## The finalize action (on ALIVE->END transition)
    ## 
    ## @return RTC::ReturnCode_t
    #
    ## 
    #def onFinalize(self):
    #

    #    return RTC.RTC_OK
	
    ###
    ##
    ## The startup action when ExecutionContext startup
    ## 
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onStartup(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The shutdown action when ExecutionContext stop
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onShutdown(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ##
    #
    # The activated action (Active state entry action)
    #
    # @param ec_id target ExecutionContext Id
    # 
    # @return RTC::ReturnCode_t
    #
    #
    def onActivated(self, ec_id):
        cv2.startWindowThread()

        return RTC.RTC_OK
	
    ##
    #
    # The deactivated action (Active state exit action)
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onDeactivated(self, ec_id):
        cv2.destroyAllWindows()

        return RTC.RTC_OK
	
    ##
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #

    def onExecute(self, ec_id):
        global timer

        if self._image_inIn.isNew():
            img = self._image_inIn.read()
            
            # CameraImage型のデータをOpenCVの形式に変換
            width = img.width
            height = img.height
            image_data = np.frombuffer(img.pixels, dtype=np.uint8)
            #print(len(img.pixels))
            #print(image_data)

            if len(img.pixels) == 0:
                print("no data")
            else:
                frame = image_data.reshape((height, width, 3))
                #print(frame)

            # バーコード検出と送信処理
                frame , productID = detect_and_draw_barcodes(frame)

                if productID == 404:
                    #print("not found")
                    timer += 1
                    if timer > 300:
                        self._d_id_out.data = productID
                        self._id_outOut.write()
                        timer = 0
                    else:
                        pass
                else:
                    self._d_id_out.data = productID
                    self._id_outOut.write()
                    timer = 0

            
            # productID を _id_outOut ポートから出力
                #self._d_id_out.data = productID
                #self._id_outOut.write()
                

            # フレームを表示
                cv2.imshow('Barcode Scanner', frame)

                if cv2.waitKey(1) & 0xFF == 27:
                    pass

        return RTC.RTC_OK
	
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onAborting(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The error action in ERROR state
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onError(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The reset action that is invoked resetting
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onReset(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The state update action that is invoked after onExecute() action
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##

    ##
    #def onStateUpdate(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The action that is invoked when execution context's rate is changed
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK


def RecogBarcodeRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=recogbarcodertc_spec)
    manager.registerFactory(profile,
                            RecogBarcodeRTC,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    RecogBarcodeRTCInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("RecogBarcodeRTC" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

