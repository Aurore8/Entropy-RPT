###IMPORT
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy import stats
import csv
import statistics
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

###CLASS AND METHODS

class Battery:
    '''
    A class used to represent a battery

    Attributes
    ----------
    name : string
       The name of the battery
    nominal_capacity : float
        The nominal capacity of the battery indicated by the constructor
    mass : float
        Mass of the battery
    Hioki_R : float
        The resistance of the battery measured by the Hioki device
    RPT_file : string 
        Path of the file containing all the data for a Reference Perfomance Test (RPT)
    impedance_file: string
        Path of the file containing all the data to study the reference impedance of a battery

    Methods
    -------
    RPT_plot()
        Display the current, OCV, temperature and capacities against the time for the RPT  of a battery
    RPT_capacity()
        Return the RPT capacity of a battery 
    get_impedance()
        Return the different caracterisation resistances of a battery (high-frequences, medium-frequences, total) '''
        
        
    def __init__(self,name,nominal_capacity,mass,resistance,RPT_file,impedance_file):
        ''' Parameters
            ---------- 
            name : string
                The name of the battery  (ex: LFP02, Samsumg10, graphite17...)
            nominal_capacity : float
                The nominal capacity of the battery indicated by the constructor (Unit: mAh)
            mass : float
                Mass of the battery (Unit:g), otherwise put 0
            Hioki_R : float
                The resistance of the battery measured by the Hioki device  (Unit: mOhm), otherwise pu 0
            RPT_file : string 
                Path of the file containing all the data for a Reference Perfomance Test (RPT), otherwise put ''
            impedance_file: string
                Path of the file containing all the data to study the reference impedance of a battery, otherwise put ''
            '''

        self.name=name
        self.nominal_capacity = nominal_capacity
        self.mass=mass
        self.Hioki_R=resistance
        self.RPT_file=RPT_file
        self.impedance_file=impedance_file
        
        
    def RPT_plot(self):
        '''Display the current, OCV, temperature and capacities against the time for the RPT  of a battery'''
        title_plot="RPT"+self.name
        fig, ax = plt.subplots()
        axes = [ax, ax.twinx(), ax.twinx(),ax.twinx()]   # Twin the x-axis twice to make independent y-axes.
        fig.subplots_adjust(right=0.65)    # Make some space on the right side for the extra y-axis
        fig.suptitle(title_plot)
        axes[2].spines['right'].set_position(('axes', 1.4))  # Move the last y-axis spine over to the right by 20% of the width of the axes
        axes[3].spines['right'].set_position(('axes', 1.2))
        # To make the border of the right-most axis visible, we need to turn the frame on. This hides the other plots, however, so we need to turn its fill off.
        axes[1].set_frame_on(True)
        axes[1].patch.set_visible(False)
        
        if self.RPT_file[-3:]=='mpt':     #Biology file
            df=pd.read_csv(self.RPT_file,header=104,sep='\t', encoding='latin-1')
            axes[3].plot(df['time/s'],df['Temperature/°C'],linestyle=':',color='gray')
            axes[3].set_ylabel('Temperature (°C)', color='gray')
            axes[3].tick_params(axis='y', colors='gray')
            axes[3].set_ylim(15,30)
            axes[0].plot(df['time/s'],df['I/mA'],color='Blue')
            axes[0].set_ylabel('Curent (mA)', color='Blue')
            axes[0].tick_params(axis='y', colors='Blue')
            axes[0].set_xlabel('Time (s)')
            axes[1].plot(df['time/s'],df['Ecell/V'],color='Red')
            axes[1].set_ylabel('Potential (V)', color='Red')
            axes[1].tick_params(axis='y', colors='Red')
            axes[2].plot(df['time/s'],df['Capacity/mA.h'],color='green')
            axes[2].set_ylabel('Capacity (mAh)', color='green')
            axes[2].tick_params(axis='y', colors='green')
            axes[2].set_ylim(-1000,1600)
            
        elif self.RPT_file[-3:]=='csv':      #Novonix file
            df=pd.read_csv(self.RPT_file,header=159)
            axes[3].plot(df['Run Time (h)'],df['Temperature (°C)'],linestyle='--',color='gray')
            axes[3].set_ylabel('Temperature (°C)', color='gray')
            axes[3].tick_params(axis='y', colors='gray')
            axes[3].set_ylim(19,21)
            axes[0].plot(df['Run Time (h)'],df['Current (A)'],color='Blue')
            axes[0].set_ylabel('Curent (A)', color='Blue')
            axes[0].tick_params(axis='y', colors='Blue')
            axes[0].set_xlabel('Time (h)')
            axes[1].plot(df['Run Time (h)'],df['Potential (V)'],color='Red')
            axes[1].set_ylabel('Potential (V)', color='Red')
            axes[1].tick_params(axis='y', colors='Red')
            axes[1].set_ylim(2.4,3.8)
            axes[2].plot(df['Run Time (h)'],df['Capacity (Ah)'],color='green')
            axes[2].set_ylabel('Capacity (Ah)', color='green')
            axes[2].tick_params(axis='y', colors='green')
            axes[2].set_ylim(-1.6,1)
        
        else:                               #basytec file
            df=pd.read_csv(self.RPT_file, header=32, encoding='latin-1')
        
        plt.shw()
            
        
    def RPT_capacity(self):
        '''Get the RPT capacity of a battery 

        Returns
        -------
        capacity: float
             RPT capacity of a battery (Unit : Ah) '''
             
        if self.RPT_file[-3:]=='mpt':     #Biology file
            df=pd.read_csv(self.RPT_file,header=104,sep='\t', encoding='latin-1')
            conversion=1000  #conversion coefficient between Ah and mAh
            capacity=max(df['Capacity/mA.h'])/conversion -min(df['Capacity/mA.h'])/conversion
        elif self.RPT_file[-3:]=='csv':      #Novonix file
            df=pd.read_csv(self.RPT_file,header=159)
            capacity=max(df['Capacity (Ah)'])-min(df['Capacity (Ah)'])
        else:                               #basytec file
            df=pd.read_csv(self.RPT_file, header=32, encoding='latin-1')
            capacity=max(df['Ah[Ah]'])-min(df['Ah[Ah]'])
        return capacity
    
    def get_impedance(self):
        ''' Get the different caracterisation resistances of a battery (high-frequences, medium-frequences, total)
        
            Returns
            -------
            R_hf: float
                High-frequences resistance (Unit : mOhm)
            R_mf: float
                Medium-frequences resistance (Unit : mOhm)
            R_t: float
                Total resistance (Unit : mOhm)'''
                
        df=pd.read_csv(self.impedance_file,header=104,sep='\t', encoding='latin-1')
        #Take off the first data and keep the accurate ones
        df2 = df[(df['Re(Z)/Ohm'] != 0.0) & (df['-Im(Z)/Ohm'] != -0.0)]
        #Find the R_hf
        df_rhf= df2[(df2['-Im(Z)/Ohm'] < 0.001) & (df2['-Im(Z)/Ohm'] > -0.001)]  #find the rows with -Im(Z)~0
        R_hf=df_rhf['Re(Z)/Ohm'].mean()*1000   #the mean Re(Z) corresponding to the rows with -Im(Z)~0 
        #Find the R_mf
        df_rmh=df2[(df2['freq/Hz'] < 0.30) & (df2['freq/Hz'] > 0.08)]   #find the rows with Freq~100mHz
        min_value_index=df_rmh['-Im(Z)/Ohm'].idxmin()   #index of the minimum value among the rows with Freq~100mHz
        R_mf=df_rmh.loc[min_value_index, 'Re(Z)/Ohm']*1000  #the Re(Z) value 
        #Find the R_t
        last_index_label=df2.index.values[len(df2)-1]
        R_t=df2.loc[last_index_label,'Re(Z)/Ohm']*1000 #the Re(Z) value of the last row (df2.tail()) 
        return R_hf,R_mf,R_t
        


class Battery_group:
    '''A class used to represent a group of battery

    Attributes
    ----------
    battery_list : list 
       List of Battery 
    weight_list : list
        List of the weight of the Batteries'''
        
    def __init__(self, battery_list):
        self.battery_list=battery_list
        weight_list=[]
        for i in range(len(battery_list)):
            weight_list.append(self.battery_list[i].mass)
        self.weight_list=weight_list
        
    def capacity_list_std(self):
        '''Get each cell discharge capacity and standard deviation and mean value from a set of battery discharge capacity
        
            Returns
            -------
            disc_caps: list
                List of the capacities from a set of Battery (Unit : Ah)
            Standart capacities deviation : float
                    (Unit : Ah)
            Mean capacity: float
                 (Unit : Ah) '''
                 
        disc_caps=[]
        for i in range(len(self.battery_list)):
            disc_caps.append(self.battery_list[i].RPT_capacity())    #get the capacity from each battery
        return (disc_caps, pd.Series(disc_caps).std(),pd.Series(disc_caps).mean())
    

    def Discharge_cap_plot(self):
        '''Display the discharge capacity of the cells list on an histogram with the standard deviation margin and the mean value '''
        disc_caps,std,m=self.capacity_list_std()
        data_table=pd.DataFrame([1,2,3,4,5,6,7,8,9,10],columns=['Cell n°'])
        data_table['Capacities']=pd.Series(disc_caps)
        fig,ax=plt.subplots()
        data_table['Capacities'].plot(kind = 'bar', color= 'lightblue',ax=ax, grid=False)
        plt.axhline(y=m, linestyle='--',color='blue', label= 'Mean value')
        plt.axhline(y=m-std,linestyle=':',color='r', label= 'Standart deviation')
        plt.axhline(y=m+std,linestyle=':',color='r')
        #ax.plot([i for i in range(0,10)],[m for i in range(0,10)],linestyle='-',color='blue', label= 'Mean value')
        #ax.plot([i for i in range(0,10)],[m-std for i in range(0,10)],linestyle=':',color='r', label= 'Standart deviation')
        #ax.plot([i for i in range(0,10)],[m+std for i in range(0,10)],linestyle=':',color='r')
        ax.set_ylabel('Discharge Capacity [Ah]')
        plt.legend(loc='best')
        plt.show()
        
    def Discharge_cap_weight_plot(self):
        '''Display the discharge capacity of the cells list on an histogram with the weight of each cell '''
        disc_caps,std,m=self.capacity_list_std()
        #Creation of the data frame, with index=cell number
        df=pd.DataFrame([1,2,3,4,5,6,7,8,9,10],columns=['Cell n°'])    
        #Add the capacity and weight series
        df['Capacities']=pd.Series(disc_caps)
        df['Weight (g)']=pd.Series(self.weight_list)
        fig,ax = plt.subplots() # Create matplotlib figure
        ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.
        width = 0.2
        df['Capacities'].plot(kind='bar', color='red', ax=ax, width=width,grid=False, position=1)
        df['Weight (g)'].plot(kind='bar', color='blue', ax=ax2, width=width,grid=False, position=0)
        ax.set_xlabel('Cell n°')
        ax.set_ylabel('Discharge Capacity (Ah)', color='red')
        ax.tick_params(axis='y', colors='red')
        ax2.set_ylabel('Weight (g)',color='blue')
        ax2.tick_params(axis='y', colors='blue')
        plt.show()
        
    def get_mean_impedance(self):
        ''' Get the mean resistances (R_hf, R_mf,R_t) from a set of Battery '''
        R_hf_list=[]
        R_mf_list=[]
        R_t_list=[]
        for i in range(len(self.battery_list)):
            R_hf,R_mf,R_t=self.battery_list[i].get_impedance()
            R_hf_list.append(R_hf)   
            R_mf_list.append(R_mf)
            R_t_list.append(R_t)
        return pd.Series(R_hf_list).mean(), pd.Series(R_mf_list).mean(), pd.Series(R_t_list).mean()
    
    def Nyquist_impedance_plot(self):
        '''Display the Nyquist diagram from a set of battery'''
        R_hf_mean,R_mf_mean,R_t_mean= self.get_mean_impedance()
        fig,ax=plt.subplots()
        for i in range(len(self.battery_list)):
            df=pd.read_csv(self.battery_list[i].impedance_file,header=104,sep='\t', encoding='latin-1')
            lab=self.battery_list[i].name
            #Take off the first data and keep the accurate ones
            df2 = df[(df['Re(Z)/Ohm'] > 0.02) & (df['-Im(Z)/Ohm'] > -0.005)]
            #plot
            ax.plot(df2['Re(Z)/Ohm'],df2['-Im(Z)/Ohm'], label=lab)
        plt.axhline(y=0, linestyle='-',color='grey')
        ax.set_ylabel('-Im(Z)/Ohm')
        ax.set_xlabel('Re(Z)/Ohm')
        plt.title("Impedance")
        plt.legend(loc='best')
        plt.show()
        
    def comparaison_impedance_plot(self):
        '''Display the different resistance (R_hf,R_mf, R_t) from a set of Battery in a bar plot'''
        R_hf_mean,R_mf_mean,R_t_mean= self.get_mean_impedance()
        Hioki_R_list=[]
        R_hf_list=[]
        R_mf_list=[]
        R_t_list=[]
        cell_name_list=[]
        for i in range(len(self.battery_list)):
            R_hf,R_mf,R_t=self.battery_list[i].get_impedance()
            R_hf_list.append(R_hf)
            Hioki_R_list.append(self.battery_list[i].Hioki_R)
            R_mf_list.append(R_mf)
            R_t_list.append(R_t)
            cell_name_list.append(self.battery_list[i].name)
        df=pd.DataFrame(cell_name_list,columns=['Cell'])
        df['Hioki R']=pd.Series(Hioki_R_list)
        df['EIS Rhf']=pd.Series(R_hf_list)
        df['EIS Rmf']=pd.Series(R_mf_list)
        df['EIS Rt']=pd.Series(R_t_list)
        df.plot(x='Cell' , y=['Hioki R','EIS Rhf','EIS Rmf','EIS Rt'], kind = 'bar', grid=False)
        plt.ylabel('Resistance (mOhm)')
        plt.legend(loc='best')
        plt.show()
        
    def Discharge_cap_weight_linear_regression(self):
        '''Display the mass in function of the discharge capacity of each cell to study the proportionality relation. Return the linear regression coefficient'''
        disc_caps,std,m=self.capacity_list_std()
   
        #Linear regression 
        lr = scipy.stats.linregress(disc_caps,self.weight_list )
        regression_coeff= lr[2]
        R='R²='+ str(regression_coeff**2)
        #Plot
        fig,ax=plt.subplots()
        ax.plot(disc_caps,self.weight_list,'o')
        y=[]
        for i in range(len(disc_caps)):
             y.append(lr[0]*sorted(disc_caps)[i]+lr[1])
        #ax.plot(sorted(disc_caps),y)
        ax.set_ylabel('Mass (g)')
        ax.set_xlabel('Capacity (Ah)')
        ax.set_ylim(35,45)
        ax.set_xlim(1.45,1.60)
        xlim = ax.get_xlim()[0]
        ylim = ax.get_ylim()[0]
        ax.text(xlim,ylim,R)
   
        plt.show()
   

        

    
class Channel:
    '''A class used to represent a channel of a Basytec device

    Attributes
    ----------
    name : string
       The name of the channel (ex: CH00, CH18)
    thermo : string
        The name of the temperature column in the data file  (ex: MEM02[C])
    OCV : string
        The name of the voltage column in the data file (ex: OCV01[V]) '''
        
    def __init__(self, name,thermo,OCV):
        self.name=name
        self.thermo = thermo
        self.OCV=OCV
    

class Experiment:
    '''
    A class used to represent an entropy experiment 

    Attributes
    ----------
    name : string
       The name of the experiment (ex: Entropy )
    experiment_type : int
        The type of the experiment (Charge : 1 / Discharge :2 )
    setup : int
        The setup of the experiment ( Work station: 1 / BatLab :2)
    battery : Battery
        The rbattery of the experiment
    channel : Channel 
        Channel of the experiment
    time_step: float
        time of a temperature step in the entropy experiment (Unit: min)
    number_temperature_level: int
        number of temperature levels in a SOC
    temp_ref: float
        Reference temperature  (Unit: °C)
    Tsteps : list 
        List of the temperature of the different steps of the entropy experiment (ex: [28,28,25,22,28])
    df_basytec : dataFrame
        DataFrame of the Basytec file 
    title: str
        Title of the experiment (ex: Entropy Charge_LFP02 (20min_28C) )
    SOC_relax_list : list of dataFrame
        List of of dataFrame where a dataFrame gathers all the data from a state of charge during the relaxation part (including the estimated voltage data from the fitting and the 
        voltage difference between the estimation and the raw data
    df_entropy_data: dataFrame
        DataFrame containing all the data from the entropy profiling (Capacity, voltage reference, best fitting method, entropy coefficient etc)
    '''
        
    def __init__(self,name,experiment_type,setup,battery,channel,time_step,number_temperature_level,temp_ref,Tsteps,basytec_file):
        '''Parameters
           ----------
            name : string
                The name of the experiment (ex: Entropy )
            experiment_type : int
                The type of the experiment (Charge : 1 / Discharge :2 )
            setup : int
                The setup of the experiment ( Work station: 1 / BatLab :2)
            battery : Battery
                The rbattery of the experiment
            channel : Channel 
                Channel of the experiment
            time_step: float
                time of a temperature step in the entropy experiment (Unit: min)
            number_temperature_level: int
                number of temperature levels in a SOC
            temp_ref: float
                Reference temperature  (Unit: °C)
            Tsteps : list 
                List of the temperature of the different steps of the entropy experiment (ex: [28,28,25,22,28])
            basytec_file: string
                path of the txt file from basytec software'''
                
        self.name=name
        self.experiment_type=experiment_type     #Charge: 1/Discharge: 2
        self.setup=setup                         #Work station: 1/Thermal bath :2
        self.battery = battery
        self.channel = channel
        self.time_step=time_step
        self.number_temperature_level=number_temperature_level
        self.temp_ref=temp_ref
        self.Tsteps=Tsteps
        if self.setup==2:
            self.df_basytec=pd.read_csv(basytec_file, header=32, encoding='latin-1')
        else:
            self.df_basytec=pd.read_csv(basytec_file,header=12,encoding='latin-1')
        if self.experiment_type==1:
            self.title=self.name+' Charge_'+self.battery.name+' ('+str(self.time_step)+'min_'+str(self.temp_ref)+'C)'
        else:
            self.title=self.name+' Discharge_'+self.battery.name+' ('+str(self.time_step)+'min_'+str(self.temp_ref)+'C)'
        
        self.SOC_relax_list,self.df_entropy_data = self.entropy_coefficient()
            
        
        
    def max_capacity(self):
        '''Return the max capacity of the battery during the experiment'''
        return self.df_basytec['Ah[Ah]'].max()

    
    def DataFrame_T_expected(self):
        '''Create the data frame containing the expected temperature profile
        
           Return
           -------
           df_temp: dataFrame
                Dataframe of 2 colums (Temperature expected(°C) and time (h)'''
                
        temp=[]
        time=[]
        start=0
        cycle_count= int(self.df_basytec.loc[self.df_basytec.index.values[len(self.df_basytec)-1],'Count'])
        for i in range(cycle_count):
            for j in range(len(self.Tsteps)):
                temp.append(self.Tsteps[j])
                time.append(start)
                temp.append(self.Tsteps[j])
                newtime=start+(self.time_step/60)
                time.append(newtime)
                start=newtime
                
        time_serie=pd.Series(time)
        temp_serie=pd.Series(temp)
        df_temp = pd.DataFrame(time, columns = ['Time(h)'])
        df_temp['Temperature']=temp_serie
        return df_temp
        
    
    def OCV_temperature_plot(self):
        '''Displays the plot showing the OCV and temperature against time '''
        
        title_plot= self.title
        fig, ax0 = plt.subplots()
        # Twin the x-axis twice to make independent y-axes.
        ax1=ax0.twinx()
        # Make some space on the right side for the extra y-axis
        fig.subplots_adjust(right=0.65)
        fig.suptitle(title_plot)
        # To make the border of the right-most axis visible, we need to turn the frame on. This hides the other plots, however, so we need to turn its fill off.
        ax1.set_frame_on(True)
        ax1.patch.set_visible(False)
        
        if self.setup==1:
            ax0.plot(self.df_basytec['~Time[h]'],(self.df_basytec[self.channel.OCV])/1000,color='Blue')   #conversion from mV to V only for the setup=1 (work station)
        else:
            ax0.plot(self.df_basytec['~Time[h]'],self.df_basytec[self.channel.OCV],color='Blue')
        ax0.set_ylabel('OCV (V)', color='Blue')
        ax0.tick_params(axis='y', colors='Blue')
        ax0.set_xlabel('Time (h)')
        
        ax1.plot(self.df_basytec['~Time[h]'],self.df_basytec[self.channel.thermo],color='firebrick')
        ax1.plot(self.DataFrame_T_expected()['Time(h)'], self.DataFrame_T_expected()['Temperature'], linestyle='-', color='pink', label='Temperature expected')
        ax1.set_ylabel('Temperature (°C)', color='firebrick')
        ax1.tick_params(axis='y', colors='firebrick')
        ax1.set_ylim(self.temp_ref-10,self.temp_ref+2)
        plt.legend(loc='best',prop={'size':12})
        plt.show()
        
        
    def bestfit_entropy_matlab_plot(self,matlab_file):
        '''Displays the plot Entropy/SOC bestfit profile
        
        Parameters
        -----------
        matlab_file : string
            Path of the matlab file containing all the entropy data'''
        
        df_matlab=pd.read_csv(matlab_file)
        fig, ax = plt.subplots()
        fig.suptitle('MATLAB_Bestfit_'+self.title)
        
        df_matlab['SOC/Depth of discharge'] =df_matlab['Charge/Discharge [mAh]']/ df_matlab['Charge/Discharge [mAh]'].max()
        #With error bar 
        #ax2.errorbar(df_matlab['SOC/Depth of discharge'],df_matlab['Bestfit Entropy [J mol-1 K-1]'],yerr=[df_matlab['Bestfit Entropy_Lower [J mol-1 K-1]'],df_matlab['Bestfit Entropy_Upper [J mol-1 K-1]']],marker='x',markerfacecolor='black',color='black',label='bestfit')
        #Without error bar
        ax.plot(df_matlab['SOC/Depth of discharge'],df_matlab['Bestfit Entropy [J mol-1 K-1]'],marker='x',markerfacecolor='black',color='black',label='bestfit')
        if self.experiment_type==1:
            ax.set_xlabel('SOC')
        else :
            ax.set_xlabel('Depth of discharge')
        ax.set_ylabel('Entropy (J.mol-1.K-1)')
        ax.legend(prop={'size':12})
        
        plt.show()
    
    def method_entropy_matlab_plot(self,matlab_file):
        '''Displays the plot Entropy/SOC profile of all the fitting method
        
        Parameters
        -----------
        matlab_file : string
            Path of the matlab file containing all the entropy data'''
            
        df_matlab=pd.read_csv(matlab_file)
        df_matlab=df_matlab.iloc[1:]
        fig, ax = plt.subplots()
        fig.suptitle('MATLAB_Method'+self.title)
        
        df_matlab['SOC/Depth of discharge'] =df_matlab['Charge/Discharge [mAh]']/ df_matlab['Charge/Discharge [mAh]'].max()
        #Without error bar
        ax.plot(df_matlab['SOC/Depth of discharge'],df_matlab['M1 Entropy [J mol-1 K-1]'],marker='x',markerfacecolor='grey',color='grey',label='Method n°1')
        ax.plot(df_matlab['SOC/Depth of discharge'],df_matlab['M2 Entropy [J mol-1 K-1]'],marker='x',markerfacecolor='green',color='green',label='Method n°2')
        ax.plot(df_matlab['SOC/Depth of discharge'],df_matlab['M3 Entropy [J mol-1 K-1]'],marker='x',markerfacecolor='darkorange',color='darkorange',label='Method n°3')
        ax.plot(df_matlab['SOC/Depth of discharge'],df_matlab['M4 Entropy [J mol-1 K-1]'],marker='x',markerfacecolor='darkviolet',color='darkviolet',label='Method n°4')
        #With errorbar
        #ax2.errorbar(df_matlab['SOC/Depth of discharge'],df_matlab['M1 Entropy [J mol-1 K-1]'],yerr=[df_matlab['M1 Entropy_Lower [J mol-1 K-1]'],df_matlab['M1 Entropy_Upper [J mol-1 K-1]']],marker='x',markerfacecolor='grey',color='grey',label='Method n°1')
        #ax2.errorbar(df_matlab['SOC/Depth of discharge'],df_matlab['M2 Entropy [J mol-1 K-1]'],yerr=[df_matlab['M2 Entropy_Lower [J mol-1 K-1]'],df_matlab['M2 Entropy_Upper [J mol-1 K-1]']],marker='x',markerfacecolor='green',color='green',label='Method n°2')
        #ax2.errorbar(df_matlab['SOC/Depth of discharge'],df_matlab['M3 Entropy [J mol-1 K-1]'],yerr=[df_matlab['M3 Entropy_Lower [J mol-1 K-1]'],df_matlab['M3 Entropy_Upper [J mol-1 K-1]']],marker='x',markerfacecolor='yellow',color='yellow',label='Method n°3')
        #ax2.errorbar(df_matlab['SOC/Depth of discharge'],df_matlab['M4 Entropy [J mol-1 K-1]'],yerr=[df_matlab['M4 Entropy_Lower [J mol-1 K-1]'],df_matlab['M4 Entropy_Upper [J mol-1 K-1]']],marker='x',markerfacecolor='hotpink',color='yellow',label='hotpink')
    
        if self.experiment_type==1:
            ax.set_xlabel('SOC')
        else :
            ax.set_xlabel('Depth of discharge')
        ax.set_ylabel('Entropy (J.mol-1.K-1)')
        ax.legend(prop={'size':12})
        
        plt.show()
        
    def rawdata_entropy_matlab_plot(self,matlab):
        '''Displays the plot Entropy/SOC rawdata profile
        
        Parameters
        -----------
        matlab_file : string
            Path of the matlab file containing all the entropy data'''
            
        df_matlab=pd.read_csv(matlab)
        fig, ax = plt.subplots()
        fig.suptitle('MATLAB_Raw data_'+self.title)
        df_matlab['SOC/Depth of discharge'] =df_matlab['Charge/Discharge [mAh]']/ df_matlab['Charge/Discharge [mAh]'].max()
        #With error bar 
        #ax.errorbar(df_matlab['SOC/Depth of discharge'],df_matlab['Raw Entropy [J mol-1 K-1]'],yerr=df_matlab['Raw Entropy Error [J mol-1 K-1]'], marker='x', markerfacecolor ='firebrick', color='firebrick')
        #Without error bar
        ax.plot(df_matlab['SOC/Depth of discharge'],df_matlab['Raw Entropy [J mol-1 K-1]'],linestyle='-',marker='x',color='firebrick',markerfacecolor ='firebrick',label='Raw_data')
        if self.experiment_type==1:
            ax.set_xlabel('SOC')
        else :
            ax.set_xlabel('Depth of discharge')
        ax.set_ylabel('Entropy (J.mol-1.K-1)')
        ax.legend(prop={'size':12})
        
        plt.show()
        
   

        
    def entropy_coefficient(self):
        ''' Isolate the SOCs and calculate the entropy coefficient
        
            Return
            -------
            SOC_relax_list : list of dataFrame
                List of of dataFrame where a dataFrame gathers all the data from a state of charge during the relaxation part (including the estimated voltage data from the fitting    
                and the voltage difference between the estimation and the raw data
            df_entropy_data: dataFrame
                DataFrame containing all the data from the entropy profiling (Capacity, voltage reference, best fitting method, entropy coefficient etc)
                
            Save
            ------
            SOC_relax_list : CSV
                save the different SOCs in different CSV files
            df_entropy_data: CSV
                save all the data from the entropy profiling in a CSV file'''
                
        ##Block 1 : Constant and parameters 
        F= 96485.3415    #Faraday's number in J.mol-1.V-1
        n=  1              #number of exchanged electron
        number_method=4     #number of different fitting method
        
        #Percentage for the fitting
        per1=0.5          #between per1% and per2% of the time and voltage of the first part of SOC_relax where temperature=temperature_reference
        per2=0.9
        per3=0.50         #between per3% and 100% of the time and voltage of the last part of SOC_relax where temperature=temperature_reference
        
        ##Block 2 : Conversion mV to V, °C to kelvin, for the bassytec file 
        if self.setup==1:                   #conversion from mV to V only for the setup=1 (work station)
            self.df_basytec['Agilent(V)']=self.df_basytec[self.channel.OCV]/1000
        else :
            self.df_basytec['Agilent(V)']=self.df_basytec[self.channel.OCV]
            
        self.df_basytec['Temperature(K)']=self.df_basytec[self.channel.thermo]+273
        
        
        ##Block 3 : Split the data in different SOC (each SOC a dataFrame) 
        #Get the total number of SOC
        SOC_total= int(self.df_basytec.loc[self.df_basytec.index.values[len(self.df_basytec)-1],'Count'])
        #get the indexes of the raws where non-zero current starts, where a new SOC starts(only raws where 'Count' and 'Cyc-Count' are different)
        index_list=[]
        index_raws=self.df_basytec[self.df_basytec['Count'] != self.df_basytec['Cyc-Count'] ]
        index_list=index_raws.index
        #Stock the SOC in a list
        SOC_list=[]
        for i in range(SOC_total):
            if i==0:                         #for the 1st soc
                SOC=self.df_basytec.iloc[0:index_list[i],:]    
            elif i==SOC_total-1:                 #for the last soc
                SOC=self.df_basytec.iloc[index_list[i-1]:index_list[-1],:]
            else:
                SOC=self.df_basytec.iloc[index_list[i-1]:index_list[i],:]
            SOC_list.append(SOC)
            
        ##Block 4 :Split the data of each SOC to keep only the relaxation part and save the indexes of the different temperature levels 
        SOC_relax_list=[]
        SOC_temp_index_list=[]
        for i in range (len(SOC_list)):
            SOC_relax=SOC_list[i][SOC_list[i]['I[A]'] == 0.0 ]   #keep the relaxation part when current=0 A   
            SOC_relax_list.append(SOC_relax)       
            SOC_temp_index=SOC_relax.loc[SOC_relax['State']==0]     #save the indexes of the different temperature levels of the SOCs
            SOC_temp_index_list.append(SOC_temp_index.index.values)
        
        

        ##Block 5 :For each SOC relax...
        SOC_capacity=[]
        SOC_OCV_reference=[]
        coef_fit_method1=[]
        coef_fit_method2=[]
        coef_fit_method3=[]
        coef_fit_method4=[]        
        MSE_method1=[]
        MSE_method2=[]
        MSE_method3=[]
        MSE_method4=[]
        entropy_method1=[] 
        entropy_method2=[]
        entropy_method3=[]
        entropy_method4=[] 
        entropy_bestfit=[] 
        entropy_rawdata=[]
        entropy_method1_error=[] 
        entropy_method2_error=[]
        entropy_method3_error=[]
        entropy_method4_error=[] 
        bestfit_method_list=[] 
        enthalpy_method1=[]
        enthalpy_method2=[]
        enthalpy_method3=[]
        enthalpy_method4=[]
        
        
        
        number_of_SOC=len(SOC_relax_list)
        for i in range (len(SOC_relax_list)):
            SOC_df =SOC_relax_list[i]    
            SOC_temp_index=SOC_temp_index_list[i]
            
            ## Block 5.1: Voltage reference 
            SOC_OCV_reference.append(SOC_df.at[SOC_df.index.values[len(SOC_df)-1],'Agilent(V)']) #keep the last voltage value of the SOC
            
            ##Block 5.2: Capacity reference
            last_index_label=SOC_df.index.values[len(SOC_df)-1]
            SOC_capacity.append(abs(SOC_df.loc[last_index_label,'Ah[Ah]']))  #keep the last capacity value of the SOC
            
            ##Block 5.3: Get the temperature levels, voltage levels_rawdata, delta_temperature
            SOC_temperature=SOC_df.loc[:,'Temperature(K)']
            SOC_voltage=SOC_df.loc[:,'Agilent(V)']
            temperature_levels=[]
            voltage_levels_rawdata=[]
            delta_E_levels=[]
            #For each temperature level
            for k in range(self.number_temperature_level):
                #temperature profile for specific soc and temperature
                temp_profile= SOC_temperature.loc[SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level+k-1]:SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level+k]]
                #voltage profile(raw data) for specific soc and temperature
                volt_profile= SOC_voltage.loc[SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level+k-1]:SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level+k]]
                #gets the 90% of the total index for a specific temperature
                idx90=int(0.9*len(temp_profile))
                #Mean value of the temperature and voltage around idx90 of the profiles for specific soc and temperature (6 points)
                temp=temp_profile.iloc[idx90-6:idx90].mean()
                volt=volt_profile.iloc[idx90-6:idx90].mean()
    
                temperature_levels.append(temp)  
                voltage_levels_rawdata.append(volt)
                
             #Delta_temperature 
            delta_temperature=[]
            for k in range(self.number_temperature_level):
                delta_temperature.append(temperature_levels[0]-temperature_levels[k])  #delta_temperature[k]=T_ref-T[k]  with T_ref=Temperature_levels[0]
            
            
            ## Block 5.4 : Data extraction for the fitting methods
            #   -Time of the full SOC: SOC_time
            SOC_time= SOC_df.loc[:,'~Time[h]']
            SOC_time_array=SOC_time.values   #converts in array to use the fitting tools of python
            
            #   -Voltage of the full SOC  : SOC_voltage
            SOC_voltage=SOC_df.loc[:,'Agilent(V)']
            SOC_voltage_array=SOC_voltage.values  #converts in array to use the fiiting tools of python
            
            #   -between per1% and per2% of the time and voltage of the first part of SOC_relax where temperature=temperature_reference
            time_first=SOC_time.loc[SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level-1] : SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level]]
            volt_first=SOC_voltage.loc[SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level-1] : SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level]]
            index_per1=int(per1*len(time_first))
            index_per2=int(per2*len(time_first))
            time_first_cut=time_first.iloc[index_per1:index_per2].values   #keep between per1 and per2 and converts in array to use the fiiting tools of python
            volt_first_cut=volt_first.iloc[index_per1:index_per2].values     #keep between per1 and per2 and converts in array to use the fiiting tools of python
            
             #   -between per3% and 100% of the time and voltage of the last part of SOC_relax where temperature=temperature_reference
            time_last=SOC_time.loc[SOC_temp_index[len(SOC_temp_index)-1]:]
            volt_last=SOC_voltage.loc[SOC_temp_index[len(SOC_temp_index)-1]:]
            index_per3=int(per3*len(time_last))
            time_last_cut=time_last.iloc[index_per3:].values     #keep between per3 and 100% and converts in array to use the fiiting tools of python
            volt_last_cut=volt_last.iloc[index_per3:].values    #keep between per3 and 100% and converts in array to use the fiiting tools of python
            
            #   -create the arrays used for the fitting 
            time_tofit=np.concatenate((time_first_cut,time_last_cut))   #time first ant time last concatenated to create one array
            volt_tofit=np.concatenate((volt_first_cut,volt_last_cut))   #volt first ant volt last concatenated to create one array
            
            
            
            ## Block 5.5 : Voltage fitting and get deltaE=voltage_rawdata-estimated volt_curve for each method
            for method in range(number_method):
                #Method 1:  y = a + b*ln(x)
                if method==0:
                    
                    coef_method1_SOC,cov_method=np.polyfit(np.log(time_tofit),volt_tofit,1,cov=True)
                    coef_fit_method1.append(coef_method1_SOC)       #save the coefficient of the function in the list coef_method1_SOC
                    
                    volt_estimation_method_SOC=np.polyval(coef_method1_SOC,np.log(SOC_time_array))  #create the estimated volt curve if there was not temperature changes 
                    SOC_df['Volt estimation method n°1 (V)']=volt_estimation_method_SOC             #add estimated volt_curve in the dataframe of the SOC_relax n°i
                    SOC_df['Delta_E method n°1 (V)']=SOC_voltage_array-volt_estimation_method_SOC   #add delta_E in the dataframe of the SOC_relax n°i
                    
                    
                    print('Method1 SOC'+str(i))
                    
                #Method 2:  y = a*exp(-b*x) + c
                #a = y(1) - y(end), since at t=0 y=C-A and the exponential is assumed to be negative exponent
                #b = by definition of settling time 2.3*tau, B is assumed to be 1/tau and the settling time is assumed to be the last time coefficient
                #c = asymptote value of the function
                def func1(x,a,b,c):
                    return a*np.exp(-b*x)+c
                if method==1:
    
                    start = [volt_tofit[0]-volt_tofit[-1], 2.3/time_tofit[-1],volt_tofit[-1]]
                    coeff_method2_SOC,cov_method= curve_fit(func1,time_tofit,volt_tofit,p0=start,maxfev=800000)
                    coef_fit_method2.append(coeff_method2_SOC)
                    
                    volt_estimation_method_SOC=func1(SOC_time_array,*coeff_method2_SOC)
                    SOC_df['Volt estimation method n°2 (V)']=volt_estimation_method_SOC
                    SOC_df['Delta_E method n°2 (V)']=SOC_voltage_array-volt_estimation_method_SOC
                    
                    
                    print('Method2 SOC'+str(i))
                    
                #Method 3 : y = a* (ln(x))² + b*ln(x) + c
                if method==2:
                    
                    coef_method3_SOC,cov_method=np.polyfit(np.log(time_tofit),volt_tofit,2,cov=True)
                    coef_fit_method3.append(coef_method3_SOC)
                    
                    volt_estimation_method_SOC=np.polyval(coef_method3_SOC,np.log(SOC_time_array))
                    coef_fit_method3.append(coef_method3_SOC)
                    SOC_df['Volt estimation method n°3 (V)']=volt_estimation_method_SOC
                    SOC_df['Delta_E method n°3 (V)']=SOC_voltage_array-volt_estimation_method_SOC
                    
                    print('Method3 SOC'+str(i))
                    
                    
                #Method 4 :y = (a*x)/(b+x) + c
                #a = asymptote end of the function y = (a*x)/(b+x)
                #b = is the time wherein y = a/2 for y = (a*x)/(b+x)
                #c = initial value for the plot
                
                def func3(x,a,b,c):
                    return (a*x)/(b+x) +c
                        
                if method==3:
                    
                    start = [volt_tofit[-1], time_tofit[0], volt_tofit[0]]
                    coeff_method4_SOC,cov_method= curve_fit(func3,time_tofit,volt_tofit,p0=start,maxfev=800000)
                    coef_fit_method4.append(coeff_method4_SOC)
                    
                    volt_estimation_method_SOC=func3(SOC_time_array,*coeff_method4_SOC)
                    SOC_df['Volt estimation method n°4 (V)']=volt_estimation_method_SOC
                    SOC_df['Delta_E method n°4 (V)']=SOC_voltage_array-volt_estimation_method_SOC
                    
                    
                    print('Method4 SOC'+str(i))
                
                
                
            ##Block 5.6 : Get MSE (Mean Square error) for each method and SOC
            #MSE=sum(residual²)/n-p=sum((y_orig - y_est)²)/n-p=sum(delta_E²)/n-p
            #y_orig= original OCV from the experiment
            #y_est= estimated OCV
            #n= number of datapoints
            #p=number of parameters (number of coefficient in the fitting method)
            
            #Methodology: 
            #   - isolate each delta_E profile (estimated-rawdata) for each level of each method
            #   - then extract the part of each profile where the relaxation effect is not visible (between 40% and 90% of each profile) and get the residual
            #   - sum all the residuals of the whole SOC and get the MSE
            
            #For each method
            for method in range(number_method):
                total_sum_residual=0
                number_datapoints=0
                
                if method==0:
                    column_delta_E='Delta_E method n°1 (V)'
                    number_parameter=len(coef_fit_method1)
                if method==1:
                    column_delta_E='Delta_E method n°2 (V)'
                    number_parameter=len(coef_fit_method2)
                if method==2:
                    column_delta_E='Delta_E method n°3 (V)'
                    number_parameter=len(coef_fit_method3)
                if method==3:
                    column_delta_E='Delta_E method n°4 (V)'
                    number_parameter=len(coef_fit_method4)
                
                #For each temperature level extract between 40% and 90% of delta_E = residual= orgininal OCV - estimated OCV
                for k in range(self.number_temperature_level):
                    delta_E_profile_method=SOC_df.loc[SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level+k-1]:SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level+k],column_delta_E]               #delta_E profile level k
                    idx40=int(0.4*len(delta_E_profile_method))  #index 40%
                    idx90=int(0.9*len(delta_E_profile_method))  #index 90%
                    residual=delta_E_profile_method.iloc[idx40:idx90]  #extraction 
                    square_residual=residual**2                       #residual²  level k
                    sum_residual= square_residual.sum()               # sum(residual²) level k
                    total_sum_residual=total_sum_residual+sum_residual   # total_sum_residual= sum( sum(residual²) level k)
                    number_datapoints=number_datapoints+len(residual)  # number_data_points= sum( size(residual) level k)
                
                MSE=total_sum_residual/(number_datapoints-number_parameter)
                print('MSE SOC'+str(i))
                
                if method==0:
                    MSE_method1.append(MSE)
                if method==1:
                    MSE_method2.append(MSE)
                if method==2:
                    MSE_method3.append(MSE)
                if method==3:
                    MSE_method4.append(MSE)
                

             ##Block 5.7: Get delta_E  for specific soc and temperature level, and for each method
            delta_E_levels=[]
            entropy_levels=[]
            #For each method
            for method in range(number_method):
                delta_E_levels_method=[]
                if method==0:
                    column_delta_E='Delta_E method n°1 (V)'
                if method==1:
                    column_delta_E='Delta_E method n°2 (V)'
                if method==2:
                    column_delta_E='Delta_E method n°3 (V)'
                if method==3:
                    column_delta_E='Delta_E method n°4 (V)'
                    
                #For each temperature level
                for k in range(self.number_temperature_level):
                    #Isolate the delta_E profile for a specific temperature level
                    delta_E_profile_method=SOC_df.loc[SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level+k-1]:SOC_temp_index[len(SOC_temp_index)-self.number_temperature_level+k],column_delta_E]
                    
                    #gets the 90% of the total index for a specific temperature
                    idx90=int(0.9*len(delta_E_profile_method))
                    
                    #Mean value of delta_E around idx90 (6 points)
                    delta_E_mean=delta_E_profile_method.iloc[idx90-6].mean()
                    
                    #Add this value of delta_E correponding to one level of temperature of method in the list delta_E_levels of  method
                    delta_E_levels_method.append(delta_E_mean)
                    
                    
                 ##Block 5.8: Get the entropy=-nF*delta_E/delta_T for specific soc, method and temperature level
                 
                #For each temperature levels, get the slope  (in the list slope_levels_method, number of slopes=number of temperature levels -1 
                entropy_levels_method=[]
                for k in range(self.number_temperature_level-1):
                    entropy= -F*(delta_E_levels_method[k+1]/delta_temperature[k+1])  #entropy= -nF * delta_E/ delta_T
                    entropy_levels_method.append(entropy)
                    
                #Add the slopes of the method in the list of slopes gathering those of each method 
                entropy_levels.append(entropy_levels_method)
               
                
                
            ##Block 5.9 : Entropy = mean(entropy_levels)  and enthalpy
            #Raw data
            coef_linear_regression_rawdata=np.polyfit(temperature_levels,voltage_levels_rawdata,1)  #get the the coefficient of the linear regression V=a*T+b whith a=entropy
            entropy_rawdata.append(F*coef_linear_regression_rawdata[0])    #add the raw data entropy coefficient of the SOC i in the list of raw data entropy coefficients
                    
            #Fit data
            for method in range(number_method):
                entropy=np.mean(np.array(entropy_levels[method]))                   # S_m= mean( S_m,k)  entropy is the average of the different value of entropy of the p temperatures levels
                print(entropy)
                
                enthalpy=entropy*(temperature_levels[0]) - F*SOC_OCV_reference[i]              #H=S*T_ref- F *volt_ref
                
                error_repetition = abs(np.std(np.array(entropy_levels[method])))      #error_repetition= standart deviation of the list of entropy levels
                entropy_error=np.sqrt( error_repetition**2)                             
                
                if method==0:
                    entropy_method1.append(entropy)
                    entropy_method1_error.append(entropy_error)
                    enthalpy_method1.append(enthalpy)
                if method==1:
                    entropy_method2.append(entropy)
                    entropy_method2_error.append(entropy_error)
                    enthalpy_method2.append(enthalpy)
                if method==2:
                    entropy_method3.append(entropy)
                    entropy_method3_error.append(entropy_error)
                    enthalpy_method3.append(enthalpy)
                if method==3:
                    entropy_method4.append(entropy)
                    entropy_method4_error.append(entropy_error)
                    enthalpy_method4.append(enthalpy)
                    
            print('Temperature_levels: ',temperature_levels)
            
            ## Block 5.10: Select the best fit for the SOC
            list_MSE_SOC=np.array([ MSE_method1[i],MSE_method2[i],MSE_method3[i],MSE_method4[i]])  
            indice_min_MSE=np.argmin(list_MSE_SOC)    #indice of the minimum MSE
            
            bestfit_method=indice_min_MSE+1          #list indice starts at 0, and method starts at 1
            bestfit_method_list.append(bestfit_method)
            if bestfit_method==1:
                entropy_bestfit.append(entropy_method1[i])
            if bestfit_method==2:
                entropy_bestfit.append(entropy_method2[i])
            if bestfit_method==3:
                entropy_bestfit.append(entropy_method3[i])
            if bestfit_method==4:
                entropy_bestfit.append(entropy_method4[i])
            
            ##Update of the SOC_relax_list with all the entropy data
            SOC_relax_list[i]=SOC_df

                
            
        ## Block 6: CSV export 
        #Export  of the SOCs
        for i in range (len(SOC_list)):
            csv_soc_name='SOC'+str(i)+'_'+self.title+'.csv'
            SOC_list[i].to_csv(csv_soc_name,index=False,header=False)
        
        
        #Export of entropycoeff
        df_entropy_data = pd.DataFrame({'Charge/Discharge [mAh]': SOC_capacity,  'OCV [V]   ': SOC_OCV_reference,'Bestfit Entropy [J mol-1 K-1]': entropy_bestfit,'Bestfit method':bestfit_method_list,'Rawdata Entropy [J mol-1 K-1]': entropy_rawdata, 'Entropy method n°1 [J mol-1 K-1]': entropy_method1, 'Error method n°1': entropy_method1_error, 'Enthalpy method n°1': enthalpy_method1,'Entropy method n°2 [J mol-1 K-1]': entropy_method2,'Error method n°2': entropy_method2_error,'Enthalpy method n°2': enthalpy_method2, 'Entropy method n°3 [J mol-1 K-1]': entropy_method3,'Error method n°3': entropy_method3_error,'Enthalpy method n°3': enthalpy_method1, 'Entropy method n°4 [J mol-1 K-1]': entropy_method4,'Error method n°4': entropy_method4_error,'Enthalpy method n°4': enthalpy_method4}, columns = ['Charge/Discharge [mAh]', 'OCV [V]   ','Bestfit Entropy [J mol-1 K-1]','Bestfit method','Rawdata Entropy [J mol-1 K-1]', 'Entropy method n°1 [J mol-1 K-1]','Error method n°1','Enthalpy method n°1','Entropy method n°2 [J mol-1 K-1]','Error method n°2', 'Enthalpy method n°2','Entropy method n°3 [J mol-1 K-1]','Error method n°3','Enthalpy method n°3','Entropy method n°4 [J mol-1 K-1]','Error method n°4','Enthalpy method n°4'])
        CSV_name=self.title+'entropycoeff.csv'
        df_entropy_data.to_csv(CSV_name,index=False)
        

        
        ##Return: SOC_relax_list,df_entropy_data
        return SOC_relax_list,df_entropy_data
        
        
        
        
        
    def entropy_plot(self,method):
        '''Plot the entropy profiles of the chosen method, or bestfit or rawdata according to the parameter 
        
           Parameters
           ---------------------------------------------------------------------
           method: int 
                All the methods 1-4: Method=0 /Method n° 1 : method=1 / Method n°2: method=2 /Method n°3: method=3 /Method n°4: method=4 / Bestfit: method=5 /Rawdata: method=6''' 
            
        df_CSV =self.df_entropy_data
        fig, ax = plt.subplots()
        fig.suptitle(self.title)
        
        if self.experiment_type==1:
            df_CSV['SOC/Depth of charge'] = df_CSV['Charge/Discharge [mAh]']/ df_CSV['Charge/Discharge [mAh]'].max()
        if self.experiment_type==2:
            df_CSV['SOC/Depth of charge'] = 1-(df_CSV['Charge/Discharge [mAh]']/ df_CSV['Charge/Discharge [mAh]'].max())
      
        if method==0:
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°1 [J mol-1 K-1]'], color='grey', marker='x', markerfacecolor ='grey',label='Method n°1')
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°2 [J mol-1 K-1]'], color='green', marker='x', markerfacecolor ='green',label='Method n°2')
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°3 [J mol-1 K-1]'], color='darkorange', marker='x', markerfacecolor ='darkorange',label='Method n°3')
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°4 [J mol-1 K-1]'], color='darkviolet', marker='x', markerfacecolor ='darkviolet',label='Method n°4')
            #ax.errorbar(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°1 [J mol-1 K-1]'],yerr=df_CSV['Error method n°1'], color='grey', marker='x', markerfacecolor ='grey',label='Method n°1')
            #ax.errorbar(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°2 [J mol-1 K-1]'],yerr=df_CSV['Error method n°2'], color='green', marker='x', markerfacecolor ='green',label='Method n°2')
            #ax.errorbar(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°3 [J mol-1 K-1]'],yerr=df_CSV['Error method n°3'], color='darkorange', marker='x', markerfacecolor ='darkorange',label='Method n°3')
            #ax.errorbar(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°4 [J mol-1 K-1]'],yerr=df_CSV['Error method n°4'], color='darkviolet', marker='x', markerfacecolor ='darkviolet',label='Method n°4')
        if method==1:
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°1 [J mol-1 K-1]'], color='grey', marker='x', markerfacecolor ='grey',label='Method n°1')
            #ax.errorbar(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°1 [J mol-1 K-1]'],yerr=df_CSV['Error method n°1'], color='grey', marker='x', markerfacecolor ='grey',label='Method n°1')
        if method==2:
             ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°2 [J mol-1 K-1]'], color='green', marker='x', markerfacecolor ='green',label='Method n°2')
             #ax.errorbar(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°2 [J mol-1 K-1]'],yerr=df_CSV['Error method n°2'], color='green', marker='x', markerfacecolor ='green',label='Method n°2')
        if method==3:
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°3 [J mol-1 K-1]'], color='darkorange', marker='x', markerfacecolor ='darkorange',label='Method n°3')
            #ax.errorbar(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°3 [J mol-1 K-1]'],yerr=df_CSV['Error method n°3'], color='darkorange', marker='x', markerfacecolor ='darkorange',label='Method n°3')
        if method==4:
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°4 [J mol-1 K-1]'], color='darkviolet', marker='x', markerfacecolor ='darkviolet',label='Method n°4')
            #ax.errorbar(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°4 [J mol-1 K-1]'],yerr=df_CSV['Error method n°4'], color='darkviolet', marker='x', markerfacecolor ='darkviolet',label='Method n°4')
        if method==5:
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Bestfit Entropy [J mol-1 K-1]'],marker='x',markerfacecolor='navy',color='navy',label='bestfit')
        if method==6:
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Rawdata Entropy [J mol-1 K-1]'], color='firebrick', marker='x', markerfacecolor ='firebrick',label='Raw data')
        
        ax.set_xlabel('SOC')
        if self.setup==2:
            ax.set_xlim(1,0)
        if self.setup==1:
            ax.set_xlim(0,1)
        ax.set_ylabel('Entropy (J.mol-1.K-1)')
        

        ax.legend(prop={'size':12})
        plt.show()
        
        
        
    def SOC_plot(self,SOC_number):
        '''Plot the potential, and temperature of the SOC n° SOC_number
        
           Parameters
           ---------------------------------------------------------------------
           SOC_number: int 
                Number of the state of charge you want to display'''
        
        #Get the total number of SOC
        SOC_total= int(self.df_basytec.loc[self.df_basytec.index.values[len(self.df_basytec)-1],'Count'])
        #get the indexes of the raws where non-zero current starts, where a new SOC starts(only raws where 'Count' and 'Cyc-Count' are different)
        index_list=[]
        index_raws=self.df_basytec[self.df_basytec['Count'] != self.df_basytec['Cyc-Count'] ]
        index_list=index_raws.index
        #Stock the SOC in a list
        SOC_list=[]
        for i in range(SOC_total):
            if i==0:                         #for the 1st soc
                SOC=self.df_basytec.iloc[0:index_list[i],:]    
            elif i==SOC_total-1:                 #for the last soc
                SOC=self.df_basytec.iloc[index_list[i-1]:index_list[-1],:]
            else:
                SOC=self.df_basytec.iloc[index_list[i-1]:index_list[i],:]
            SOC_list.append(SOC)
        #Plot the SOC n°number SOC
        title_plot= 'SOC n°'+str(SOC_number)+'  ' +self.title
        fig, ax0 = plt.subplots()
        ax1=ax0.twinx()
        fig.subplots_adjust(right=0.65)
        fig.suptitle(title_plot)
        ax1.set_frame_on(True)
        ax1.patch.set_visible(False)
        if self.setup==1:
            ax0.plot(SOC_list[SOC_number]['~Time[h]'],(SOC_list[SOC_number][self.channel.OCV])/1000,color='Blue')   #conversion from mV to V only for the setup=1 (work station)
        else:
            ax0.plot(SOC_list[SOC_number]['~Time[h]'],SOC_list[SOC_number][self.channel.OCV],color='Blue')
        ax0.set_ylabel('OCV (V)', color='Blue')
        ax0.tick_params(axis='y', colors='Blue')
        ax0.set_xlabel('Time (h)')
        
        ax1.plot(SOC_list[SOC_number]['~Time[h]'],SOC_list[SOC_number][self.channel.thermo],color='firebrick')
        ax1.set_ylabel('Temperature (°C)', color='firebrick')
        ax1.tick_params(axis='y', colors='firebrick')
        ax1.set_ylim(self.temp_ref-10,self.temp_ref+2)
        plt.legend(loc='best',prop={'size':12})
        plt.show()
    

        
    def SOC_relax_fit_plot(self,SOC_number,method):
        '''Plot the OCV, fitted OCV and temperature of the relaxation part of the SOC n° SOC_number
        
           Parameters
           ---------------------------------------------------------------------
            SOC_number: int 
                Number of the state of charge you want to display
            method: int 
                All the methods 1-4: Method=0 /Method n° 1 : method=1 / Method n°2: method=2 /Method n°3: method=3 /Method n°4: method=4 '''
                
        SOC=self.SOC_relax_list[SOC_number]
        SOC=SOC.iloc[3:]
        title_plot= 'SOC n°'+str(SOC_number)+'  ' +self.title
        fig, ax0 = plt.subplots()
        ax1=ax0.twinx()
        fig.subplots_adjust(right=0.65)
        fig.suptitle(title_plot)
        ax1.set_frame_on(True)
        ax1.patch.set_visible(False)
        
        ax0.plot(SOC['~Time[h]'],SOC['Agilent(V)'],color='Blue')  
        if method==0:
            ax0.plot(SOC['~Time[h]'],SOC['Volt estimation method n°1 (V)'], ls='--',color='grey',label='Method n°1')
            ax0.plot(SOC['~Time[h]'],SOC['Volt estimation method n°2 (V)'], ls='--',color='green',label='Method n°2')
            ax0.plot(SOC['~Time[h]'],SOC['Volt estimation method n°3 (V)'], ls='--',color='darkorange',label='Method n°3')
            ax0.plot(SOC['~Time[h]'],SOC['Volt estimation method n°4 (V)'], ls='--',color='darkviolet',label='Method n°4')
        if method==1:
            ax0.plot(SOC['~Time[h]'],SOC['Volt estimation method n°1 (V)'], ls='--',color='grey',label='Method n°1')
        if method==2:
            ax0.plot(SOC['~Time[h]'],SOC['Volt estimation method n°2 (V)'], ls='--',color='green',label='Method n°2')
        if method==3:
            ax0.plot(SOC['~Time[h]'],SOC['Volt estimation method n°3 (V)'], ls='--',color='darkorange',label='Method n°3')
        if method==4:
            ax0.plot(SOC['~Time[h]'],SOC['Volt estimation method n°4 (V)'], ls='--',color='darkviolet',label='Method n°4')
        ax0.legend(loc='best',prop={'size':12})
        ax0.set_ylabel('OCV (V)', color='Blue')
        ax0.tick_params(axis='y', colors='Blue')
        ax0.set_xlabel('Time (h)')
            
        ax1.plot(SOC['~Time[h]'],SOC[self.channel.thermo],color='firebrick')
        ax1.set_ylabel('Temperature (°C)', color='firebrick')
        ax1.tick_params(axis='y', colors='firebrick')
        ax1.set_ylim(self.temp_ref-10,self.temp_ref+2)
        plt.show()
        
        
    def enthalpy_plot(self,method):
        '''Plot the enthalpy profiles of the chosen method
        
           Parameters
           ---------------------------------------------------------------------
           method: int 
                All the methods 1-4: Method=0 /Method n° 1 : method=1 / Method n°2: method=2 /Method n°3: method=3 /Method n°4: method=4 ''' 
            
        df_CSV =self.df_entropy_data
        fig, ax = plt.subplots()
        fig.suptitle('Enthalpy_'+self.title)
        
        if self.experiment_type==1:
            df_CSV['SOC/Depth of charge'] = df_CSV['Charge/Discharge [mAh]']/ df_CSV['Charge/Discharge [mAh]'].max()
        if self.experiment_type==2:
            df_CSV['SOC/Depth of charge'] = 1-(df_CSV['Charge/Discharge [mAh]']/ df_CSV['Charge/Discharge [mAh]'].max())
        
        if method==0:
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Enthalpy method n°1'], color='grey', marker='x', markerfacecolor ='grey',label='Method n°1')
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Enthalpy method n°2'], color='green', marker='x', markerfacecolor ='green',label='Method n°2')
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Enthalpy method n°3'], color='darkorange', marker='x', markerfacecolor ='darkorange',label='Method n°3')
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Enthalpy method n°4'], color='darkviolet', marker='x', markerfacecolor ='darkviolet',label='Method n°4')
        if method==1:
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Enthalpy method n°1'], color='grey', marker='x', markerfacecolor ='grey',label='Method n°1')
        if method==2:
             ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Enthalpy method n°2'], color='green', marker='x', markerfacecolor ='green',label='Method n°2')
        if method==3:
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Enthalpy method n°3'], color='darkorange', marker='x', markerfacecolor ='darkorange',label='Method n°3')
        if method==4:
            ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Enthalpy method n°4'], color='darkviolet', marker='x', markerfacecolor ='darkviolet',label='Method n°4')
        
        ax.set_xlabel('SOC')
        if self.setup==2:
            ax.set_xlim(1,0)
        if self.setup==1:
            ax.set_xlim(0,1)
        ax.set_ylabel('Enthalpy (J.mol-1)')
        

        ax.legend(prop={'size':12})
        plt.show()
        




       
class Experiment_group:
    '''
    A class used to represent a group of experiments 

    Attributes
    ----------
    experiment_list : list of Experiment
       The list of Experiments 
    experiment_type : int
        The type of the experiment (Charge : 1 / Discharge :2 )'''
        
    def __init__(self,experiment_type,experiment_list):
        '''Parameters
           ----------
            experiment_list : list of Experiment
                The list of Experiments 
            experiment_type : int
                The type of the experiment (Charge : 1 / Discharge :2 )'''
        self.experiment_list=experiment_list
        self.experiment_type=experiment_type

    def temperature_plot(self):
        '''Display the plot showing the evolution of the temperaure given by the thermocouples of each experiment from the attribute list_experiment'''
        fig,ax=plt.subplots()
        fig.suptitle("Temperature profiles ")
        #Plot temperature channel
        for i in range(len(self.experiment_list)):
            temperature_column= self.experiment_list[i].channel.thermo
            self.experiment_list[i].df_basytec.plot(x='~Time[h]',y=[temperature_column],ax=ax,subplots =True,c=np.random.rand(3,))
        #Plot temperature expected
        self.experiment_list[i].DataFrame_T_expected().plot(x='Time(h)',y='Temperature',ax=ax,subplots =True,c='black', label='T expected')
        plt.xlabel('Time (h)')
        plt.ylabel('Temperature (°C)')
        plt.legend(loc='best')
        plt.ylim(20,40)
        plt.show()
        
    def entropy_plot(self,method):
        '''Display the entropy profiles of different experiment in one plot
        
           Parameters
           ---------------------------------------------------------------------
            SOC_number: int 
                Number of the state of charge you want to display
            method: int 
                All the methods 1-4: Method=0 /Method n° 1 : method=1 / Method n°2: method=2 /Method n°3: method=3 /Method n°4: method=4 '''
                
        fig, ax = plt.subplots()
        fig.suptitle('Entropy profiles_Method n°'+str(method))
        for i in range(len(self.experiment_list)):
            df_CSV=self.experiment_list[i].df_entropy_data
            
            if self.experiment_type==1:
                df_CSV['SOC/Depth of charge'] = df_CSV['Charge/Discharge [mAh]']/ df_CSV['Charge/Discharge [mAh]'].max()
                a='Charge_'

            if self.experiment_type==2:
                df_CSV['SOC/Depth of charge'] = 1-(df_CSV['Charge/Discharge [mAh]']/ df_CSV['Charge/Discharge [mAh]'].max())
                a='Dicharge_'
            lab=a+str(self.experiment_list[i].time_step)+'min_'+str(self.experiment_list[i].temp_ref)+'°C'
            c=np.random.rand(3,)
            
            if method==1:
                ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°1 [J mol-1 K-1]'], color=c, marker='x', markerfacecolor =c,label=lab)
            if method==2:
                ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°2 [J mol-1 K-1]'], color=c, marker='x', markerfacecolor =c,label=lab)
            if method==3:
                ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°3 [J mol-1 K-1]'], color=c, marker='x', markerfacecolor =c,label=lab)
            if method==4:
                ax.plot(df_CSV['SOC/Depth of charge'],df_CSV['Entropy method n°4 [J mol-1 K-1]'], color=c, marker='x', markerfacecolor =c,label=lab)
            
        ax.set_xlabel('SOC')
        if self.experiment_list[0].setup==2:
            ax.set_xlim(1,0)
        if self.experiment_list[0].setup==1:
            ax.set_xlim(0,1)
        ax.set_ylabel('Entropy (J.mol-1.K-1)')
        ax.set_xlim(1,0)
        ax.legend(prop={'size':12})
        plt.show()
        
    


###Main check




            