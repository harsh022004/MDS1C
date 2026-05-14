package assign_3_cloudsim;
import org.cloudbus.cloudsim.*;
import org.cloudbus.cloudsim.core.CloudSim;
import org.cloudbus.cloudsim.provisioners.*;
import java.text.DecimalFormat;
import java.util.*;
public class scheduler {
    private static List<Cloudlet> cloudletList;
    private static List<Vm> vmList;
    @SuppressWarnings("unused")
public static void main(String[] args) {
        Log.printLine("Hello,Harshad Lohakare,Starting Your Cloud Scheduler");
        try {
            int numUsers = 1;
            Calendar calendar = Calendar.getInstance();
            boolean traceFlag = false;
            CloudSim.init(numUsers, calendar, traceFlag);
            Datacenter datacenter = createDatacenter("Datacenter_0");
            DatacenterBroker broker = createBroker();
            int brokerId = broker.getId();
            Vm vm = new Vm(0, brokerId, 1000, 1, 512, 1000, 10000, "Xen", new CloudletSchedulerTimeShared());
            vmList = Collections.singletonList(vm);
            broker.submitVmList(vmList);
            Cloudlet cloudlet = new Cloudlet(0, 400000, 1, 300, 300, new UtilizationModelFull(), new UtilizationModelFull(), new UtilizationModelFull());
            cloudlet.setUserId(brokerId);
            cloudletList = Collections.singletonList(cloudlet);
            broker.submitCloudletList(cloudletList);
            broker.bindCloudletToVm(cloudlet.getCloudletId(), vm.getId());  
            CloudSim.startSimulation();
            CloudSim.stopSimulation();
            List<Cloudlet> finishedCloudlets = broker.getCloudletReceivedList();
            printCloudletList(finishedCloudlets);
            Log.printLine("Your Cloud Scheduler finished!");
        } catch (Exception e) {
            e.printStackTrace();
            Log.printLine("Unwanted errors happen");
        }
    }
    private static Datacenter createDatacenter(String name) {
        List<Host> hostList = new ArrayList<>();
        List<Pe> peList = new ArrayList<>();
        peList.add(new Pe(0, new PeProvisionerSimple(1000)));
        hostList.add(new Host(0, new RamProvisionerSimple(2048), new BwProvisionerSimple(10000), 1000000, peList, new VmSchedulerTimeShared(peList)));
        LinkedList<Storage> storageList = new LinkedList<>();
        DatacenterCharacteristics characteristics = new DatacenterCharacteristics("x86", "Linux", "Xen", hostList, 10.0, 3.0, 0.05, 0.001,0.0);
        Datacenter datacenter = null;
        try {
            datacenter = new Datacenter(name, characteristics, new VmAllocationPolicySimple(hostList), storageList, 0);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return datacenter;
    }
    private static DatacenterBroker createBroker() {
        try {
            return new DatacenterBroker("Broker");
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
    @SuppressWarnings("deprecation")
private static void printCloudletList(List<Cloudlet> list) {
        Log.printLine();
        Log.printLine("========== OUTPUT ==========");
        Log.printLine("Cloudlet ID\tSTATUS\tData center ID\tVM ID\tTime\tStart Time\tFinish Time");
        DecimalFormat dft = new DecimalFormat("###.##");
        for (Cloudlet cloudlet : list) {
            Log.printLine(cloudlet.getCloudletId() + "\t\t" + Cloudlet.getStatusString(cloudlet.getCloudletStatus()) +
                    "\t\t" + cloudlet.getResourceId() + "\t\t" + cloudlet.getVmId() + "\t\t" +
                    dft.format(cloudlet.getActualCPUTime()) + "\t\t" + dft.format(cloudlet.getExecStartTime()) +
                    "\t\t" + dft.format(cloudlet.getFinishTime()));
        }
    }
}
