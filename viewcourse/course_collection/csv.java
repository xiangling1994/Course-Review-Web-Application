package csvConvert;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.Scanner;
import java.util.StringTokenizer;

public class csv {
	public static void main(String[]args) throws FileNotFoundException{
		
		String path  = "/Users/WZ/Documents/workspace/csvConvert/DalCourses/";
		int count1 = 0;
		
		File folder = new File("/Users/WZ/Documents/workspace/csvConvert/DalCourses");
		File[] listOfFiles = folder.listFiles();
		
		PrintWriter pw = new PrintWriter(new File("test.csv"));
		//PrintWriter pw = new PrintWriter(new FileOutputStream(new File("test.csv"), true));
        StringBuilder sb = new StringBuilder();
        
        String lastline = "";
        
        for (int i = 0; i < listOfFiles.length; i++) {
        	if (listOfFiles[i].isFile()) {
        		
        		Scanner scanner1 = new Scanner(listOfFiles[i]);

				while (scanner1.hasNextLine()) {
					String line = scanner1.nextLine();
					StringTokenizer st = new StringTokenizer(line," "); 
					if (st.countTokens() > 2){
						if (!line.equals(lastline)){
							sb.append(st.nextToken());
							sb.append(" ");
							sb.append(st.nextToken());
							sb.append(',');
							while (st.hasMoreTokens()) {  
								sb.append(st.nextToken()); 
								sb.append(" ");
						    }
							sb.deleteCharAt(sb.length()-1);
							sb.append(',');
							String filename = listOfFiles[i].getName();
							filename = filename.substring(0, filename.length()-1);
							filename = filename.substring(0, filename.length()-1);
							filename = filename.substring(0, filename.length()-1);
							filename = filename.substring(0, filename.length()-1);
							sb.append(filename);
							sb.append('\n');
						}
						lastline = line;
					}
					if (st.countTokens() == 2){
						if (!line.equals(lastline)){
							sb.append(line);
							sb.append('\n');
						}
						lastline = line;
					}
				}
		
        	}
        }
		pw.write(sb.toString());
        pw.close();
        
        System.out.println("Done!");
	}
}
