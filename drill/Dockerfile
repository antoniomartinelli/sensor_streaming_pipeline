FROM apache/drill:latest

COPY ./mongo.sys.drill /tmp/drill/sys.storage_plugins/mongo.sys.drill

#RUN wget "http://package.mapr.com/tools/MapR-ODBC/MapR_Drill/MapRDrill_odbc_v1.5.1.1002/maprdrill-1.5.1.1002-1.el7.x86_64.rpm"

#RUN apt update
#RUN apt install alien dpkg-dev debhelper build-essential alien dpkg-dev debhelper build-essential -y
#RUN alien mapdrill*

#WORKDIR /tmp
#COPY ./maprdrill_1.5.1-2_amd64.deb /tmp/maprdrill_1.5.1-2_amd64.deb
#RUN dpkg -i mapdrill*

#ENV ODBCINI=~/odbc.ini
#ENV MAPRDRILLINI=~/mapr.drillodbc.ini
#ENV LD_LIBRARY_PATH=/usr/local/lib

#COPY /opt/mapr/drill/Setup/* /root/. 



