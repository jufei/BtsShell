package ute_fault;
import static java.lang.String.format;

import java.io.IOException;
import java.net.UnknownHostException;
import java.net.InetAddress;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import com.nsn.oam.infomodel.communication.network2.alarms.AlarmSender;
import com.nsn.oam.infomodel.communication.network2.ConnectionProperties;
import com.nsn.oam.infomodel.communication.network.sic.SicConnector;
import com.nsn.oam.infomodel.communication.network.sic.messages.FaultReq;
import com.nsn.oam.infomodel.communication.network.sic.messages.GenericSoapFault;
import com.nsn.oam.infomodel.communication.network.sic.messages.SoapData;
import com.nsn.oam.infomodel.communication.network.sic.Tools;
import javax.xml.soap.*;
import javax.xml.soap.SOAPBodyElement;


public class FaultTrigger {

    private String address;
    private Integer port;
    private Integer retryCount;
    private Boolean autoReconnect;
    private ConnectionProperties connectionProperties;
    private SicConnector sicConnector;


    private static final String SOAP_SICAD = "0x1011000C";
    private static final String FAULT_ID = "faultId";
    private static final String FAULT_SOURCE = "faultSource";
    private static final String FAULT_SEVERITY = "faultSeverity";
    private static final String FAULT_STATE = "faultState";
    private static final String FAULT_TEXT = "faultText";
    private static final String EVENT_TIME = "eventTime";
    private static final String AFFECTED_OBJECTS = "affectedObjects";
    private static final String NAME = "name";

    private static final String AFFECTED_OBJECTS_SPLITTER = ",";
    private static final String HEADER_ACTION = "OBSAI_FM";
    private static final int HEADER_ID = 0;
    private static final String HEADER_RELATES_TO = "0";
    private static final String HEADER_TO = "LBTS_OM";
    private static final String HEADER_VERSION = "1.0";

    private static final SimpleDateFormat DATE_FORMAT = new SimpleDateFormat("yyyy-MM-dd");
    private static final SimpleDateFormat TIME_FORMAT = new SimpleDateFormat("hh:mm:ss");


    public FaultTrigger() {
        this.address = "192.168.255.1";
        this.port = 12347;
        this.autoReconnect = true;
        this.retryCount = 5;
    }

    public void setup_fault_trigger(String address, Integer port) throws UnknownHostException, IOException {
        this.address = address;
        this.port = port;
        this.connectionProperties = new ConnectionProperties(InetAddress.getByName(this.address), this.port, false, this.autoReconnect, this.retryCount, false);
    }

    public void teardown_fault_trigger() throws IOException {
        /* This method exists to stay backward compatible. Now each method connect and disconnect connection.
           In such case teardown method is not needed at all.
        */
    }

    public void send_saa_pro_ce_memory_over_load_ind_msg(int sender, int receiver, int status, int memory_usage) throws UnknownHostException, IOException {
        this.createConnection();
        AlarmSender alarmSender = this.createAlarmSender();
        alarmSender.sendSAaProCeMemoryOverloadIndMsg(sender, receiver, status, memory_usage);
        this.removeConnection();
    }

    public void send_saa_pro_ce_cpu_load_over_load_ind_msg(int sender, int receiver, int status, int type, int normal_cpu_load, int background_cpu_load, int irq_cpu_load) throws UnknownHostException, IOException{
        this.createConnection();
        AlarmSender alarmSender = this.createAlarmSender();
        alarmSender.sendSAaProCeCpuLoadOverloadIndMsg(sender, receiver, status, type, normal_cpu_load, background_cpu_load,irq_cpu_load);
        this.removeConnection();
    }

    public void send_hwapi_api_alarm_msg(int sender, int receiver, int fault_id, int unit_id, String... args) throws UnknownHostException, IOException {
        int[] newArgs = new int[args.length];
        for(int i=0;i<args.length; i++) {
            System.out.println("Args["+i+" "+args[i]);
            newArgs[i] = Integer.parseInt(args[i]);
        }

        this.createConnection();
        AlarmSender alarmSender = this.createAlarmSender();
        alarmSender.sendHWAPIFaultSpoofSenderAndReceiver(sender, receiver, fault_id, unit_id, newArgs);
        this.removeConnection();
    }

    public void send_hwapi_send_fault_report(int sender, int receiver, int fault_id, int unit_id, int state, int severity, int object_type, String... args) throws UnknownHostException, IOException {
        int[] newArgs = new int[args.length];
        for(int i=0;i<args.length; i++) {
            System.out.println("Args["+i+" "+args[i]);
            newArgs[i] = Integer.parseInt(args[i]);
        }

        this.createConnection();
        AlarmSender alarmSender = this.createAlarmSender();
        alarmSender.sendDSPHWAPIFault(sender, receiver, fault_id, unit_id, state, severity, object_type, newArgs);
        this.removeConnection();
    }


    public void send_lom_fault_ind_msg(int sender, int receiver, int fault_id, int fault_state, int fault_severity, int location_type, int fault_location, String... args) throws UnknownHostException, IOException {
        int[] newArgs = new int[args.length];
        for(int i=0;i<args.length; i++) {
            System.out.println("Args["+i+" "+args[i]);
            newArgs[i] = Integer.parseInt(args[i]);
        }

        this.createConnection();
        AlarmSender alarmSender = this.createAlarmSender();
        alarmSender.sendLomFault(sender, fault_id, fault_state, fault_severity, location_type, fault_location, newArgs);
        this.removeConnection();
    }

    public void send_lom_fault_req_msg(int fault_id, int unit_id, int subunit_id, int cp_id, int state, int severity, int object_type, int detecting_unit, int detecting_subunit, String... args) throws UnknownHostException, IOException {
        int[] newArgs = new int[args.length];
        for(int i=0;i<args.length; i++) {
            System.out.println("Args["+i+" "+args[i]);
            newArgs[i] = Integer.parseInt(args[i]);
        }

        FaultReq faultReq = new FaultReq(fault_id);
        faultReq = faultReq.setFaultyUnit(unit_id);
        faultReq = faultReq.setFaultySubUnit(subunit_id);
        faultReq = faultReq.setFaultyCpid(cp_id);
        faultReq = faultReq.setFaultState(state);
        faultReq = faultReq.setFaultSeverity(severity);
        faultReq = faultReq.setObjectType(object_type);
        faultReq = faultReq.setDetectingUnit(detecting_unit);
        faultReq = faultReq.setDetectingSubUnit(detecting_subunit);
        faultReq = faultReq.setFaultInfo(newArgs);

        this.createConnection();
        AlarmSender alarmSender = this.createAlarmSender();
        alarmSender.sendFaultReq(faultReq);
        this.removeConnection();
    }


    public void send_soap_rp1_fault_report(String sender, int fault_id, String from, String source, String affected_objects, String severity, String state, String text, String... args) throws UnknownHostException, IOException, SOAPException {
        SoapData sd = new SoapData();
        sd = sd.setAction(HEADER_ACTION);
        sd = sd.setFrom(from);
        sd = sd.setId(HEADER_ID);
        sd = sd.setRelatesTo(HEADER_RELATES_TO);
        sd = sd.setTo(HEADER_TO);
        sd = sd.setVersion(HEADER_VERSION);

        SOAPBodyElement body = sd.addAlarmNotif();
        createAffectedObjectsList(body, affected_objects);

        body.addChildElement(EVENT_TIME).setValue(createStringFromGivenDate(new Date()));
        body.addChildElement(FAULT_ID).setValue(String.valueOf(fault_id));
        body.addChildElement(FAULT_SEVERITY).setValue(severity);
        body.addChildElement(FAULT_SOURCE).setValue(source);
        body.addChildElement(FAULT_STATE).setValue(state);
        body.addChildElement(FAULT_TEXT).setValue(text);

        GenericSoapFault gsf = new GenericSoapFault();
        gsf.setContent(sd);

        this.createConnection();
        AlarmSender alarmSender = this.createAlarmSender();
        alarmSender.sendSoapFault(convert_sender(sender), gsf);
        this.removeConnection();
    }

    private void createAffectedObjectsList(SOAPBodyElement body, String affectedObjectsParam) throws SOAPException {
        String[] affectedObjectsArray = getArrayOfAffectedObjects(affectedObjectsParam);

        SOAPElement affectedObjects = body.addChildElement(AFFECTED_OBJECTS);
        for (String s : affectedObjectsArray)
            affectedObjects.addChildElement(NAME).setValue(s);
    }

    private String[] getArrayOfAffectedObjects(String paramValueAsString) {
        return paramValueAsString.split(AFFECTED_OBJECTS_SPLITTER);
    }

    private String createStringFromGivenDate(Date givenDate) {
        String date = DATE_FORMAT.format(givenDate);
        String time = TIME_FORMAT.format(givenDate);
        return format("%sT%s+00:00", date, time);
    }

    private int convert_sender(String sender) {
        return Tools.getSicAddressBasedOnIp(sender);
    }

    private int[] convert_to_int_array(String[] array) {
        int[] newArray = new int[array.length];
        for(int i=0;i<array.length; i++) {
            newArray[i] = Integer.parseInt(array[i]);
        }
        return newArray;
    }

    private AlarmSender createAlarmSender() throws UnknownHostException, IOException {
        AlarmSender alarmSender = new AlarmSender();
        alarmSender.setSicConnector(this.sicConnector);
        return alarmSender;
    }

    private void createConnection() throws UnknownHostException, IOException {
        this.sicConnector = connectionProperties.getSicConnector();
    }

    private void removeConnection() {
        this.sicConnector.disconnect();
    }
}
