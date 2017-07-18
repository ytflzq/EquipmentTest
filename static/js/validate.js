function validate_text(name, msg) {
	//var re = /^[ a-zA-Z0-9\u0391-\uFFE5\~!@#\$\^\*\(\)\-_\{\}\|:;\/\.]*$/;
	var re= /^[ a-zA-Z0-9\u0391-\uff0b\uff0d-\uFFE5\~!@#\$\^\*\(\)\-_\{\}:;\/\.]*$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	alert(msg);
	return false;
}

//检查用户管理用户名
function validate_username(name, msg){
    var reg = /[+\\/\"\'<>&;%\*,]/;
    var value = document.getElementsByName(name)[0].value;
    if(reg.test(value) || get_utf8length(value)>60){
        alert(msg);
        return false;
    }
    return true;
}

//检查IPSEC用户名
function validate_ipsec_username(name, msg) {
    var reg = /[\u0391-\uFFE5+\/\\"'<>&;%\*\s]/;
    var value = document.getElementsByName(name)[0].value;
    if(reg.test(value) || get_utf8length(value)>60){
        alert(msg);
        return false;
    }
    return true;
}

//检查sslvpn网关用户名
function validate_sslvpngw(name, msg){
    var reg = /[+\\/\"\'<>&;%\*,]/;
    var value = document.getElementsByName(name)[0].value;
    if(reg.test(value) || value.length>60){
        alert(msg);
        return false;
    }
    return true;
}

//检查数据库下危险字符
function validate_text_db(name, msg) {
	var re = /^[ a-zA-Z0-9\u0391-\uFFE5\(\)\-_\{\}:\.,]*$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	alert(msg);
	return false;
}

//检查邮箱
function validate_email(name, msg){
    var re = /^\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]*\.)+[A-Za-z]{2,14}$/;
    var item = document.getElementsByName(name)[0].value;
    if (re.test(item)) {
        return true;
    }
    alert(msg);
    return false;
}


function validate_domain(name) {
	var re = /^([a-zA-Z0-9\-]+\.)+[a-zA-Z0-9\-]+$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	return false;
}

function validate_list(name, msg) {
	items = document.getElementsByName(name+'[]');
	for (i = 0; i < items.length; i++) {
		if (items[i].checked) {
			return true;
		}
	}
	if(msg !== undefined){
		alert(msg);
	}
	return false;
}

function validate_ip(name, msg) {
	var re = /^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	alert(msg);
	return false;
}
//和上面一个方法一样，少的只是一个mes
function validate_ip2(name) {
    var re = /^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$/;
    var item = document.getElementsByName(name)[0].value;
    if (re.test(item)) {
        return true;
    }
    return false;
}
function validate_ip4(name) {
	var re = /^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\/([0-9]{1}|[0-2][0-9]|3[0-2])){0,1}$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	return false;
}
function validate_ip4_nomask(name) {
	var re = /^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	return false;
}
function validate_ip4_mask(name) {
	var re = /^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\/([0-9]{1}|[0-2][0-9]|3[0-2]))$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	return false;
}
//fixed Bug 118974 组播 广播  0.0.0.0  和*.0.0.0  *.*.0.0 *.*.*.0之外的单播地址为合法ip4 
function validate_ip4_special(value){
    if (value=="0.0.0.0/0") {
        return false;
    }
    value = value.split('/')[0];
    //0.0.0.0 *.0.0.0 *.*.0.0 *.*.*.0
    var re = /^(0\.0\.0\.0)|((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.0\.0\.0)|(((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){2}0\.0)|(((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}0)$/;
    if (re.test(value)) {
        return true;
    }

    //组播224.0.0.0~239.255.255.255
    var re_multicast = /^((22[4-9]|23[0-9])\.)((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){2}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$/;
    if(re_multicast.test(value)){
        return true;
    }

    //广播*.*.*.255 *.*.255.255 *.255.255.255 255.255.255.255
    var re_broadcast = /^(255\.255\.255\.255)|((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.255\.255\.255)|(((25[0-4]|2[0-5][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){2}255\.255)|(((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}255)$/;
    if (re_broadcast.test(value)) {
        return true;
    }

    return false;
}
// Bug 121317 - 【接口 - web】接口IP地址输入未对特殊IP进行校验
// a、广播地址：255.255.255.255/24
// b、本机地址：127.0.0.1/24
// c、组播地址：224.0.0.1/24-239.255.255.255/24
function validate_ip4_special2(value){
    if (value=="0.0.0.0/0") {
        return false;
    }
    //网络地址：120.120.0.0/16   
    var ms = parseInt(value.split('/')[1]);
    var msip ="";
    for (var j = ms; j > 0; j--) {
        msip+="1";
    }
    for (var j = 32-ms; j > 0; j--) {
        msip+="0";
    }
    var ip = value.split('/')[0];
    var arr = ip.split('.');
    var ipstr =""
    for(var i=0;i<arr.length;i++){
        var str ="";
        for (var j = 8; j > parseInt(arr[i]).toString(2).length; j--) {
            str+="0";
        }
        str+=parseInt(arr[i]).toString(2);
        ipstr+=str;
    }
    var  resultip = "";
    for (var i = 0; i < ipstr.length; i++) {
        console.log(msip[i]);
        if (msip[i]=="1") {
            resultip+="0";
        }else{
            resultip+=ipstr[i];
        }
    }
    if (parseInt(resultip)==0) {
        return true;
    }

    value = value.split('/')[0];
    if (value=="127.0.0.1") {
        return true;
    }
    //组播224.0.0.0~239.255.255.255
    var re_multicast = /^((22[4-9]|23[0-9])\.)((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){2}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$/;
    if(re_multicast.test(value)){
        return true;
    }

    //广播*.*.*.255 *.*.255.255 *.255.255.255 255.255.255.255
    var re_broadcast = /^(255\.255\.255\.255)|((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.255\.255\.255)|(((25[0-4]|2[0-5][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){2}255\.255)|(((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}255)$/;
    if (re_broadcast.test(value)) {
        return true;
    }

    return false;
}
// Bug 121317 - 【接口 - web】接口IP地址输入未对特殊IP进行校验
// d、网络地址：120.120.0.0/16
function validate_ip4_net(value){
    if (value=="0.0.0.0/0") {
        return false;
    }
    //网络地址：120.120.0.0/16   
    var ms = parseInt(value.split('/')[1]);
    var msip ="";
    for (var j = ms; j > 0; j--) {
        msip+="1";
    }
    for (var j = 32-ms; j > 0; j--) {
        msip+="0";
    }
    var ip = value.split('/')[0];
    var arr = ip.split('.');
    var ipstr =""
    for(var i=0;i<arr.length;i++){
        var str ="";
        for (var j = 8; j > parseInt(arr[i]).toString(2).length; j--) {
            str+="0";
        }
        str+=parseInt(arr[i]).toString(2);
        ipstr+=str;
    }
    var  resultip = "";
    for (var i = 0; i < ipstr.length; i++) {
        console.log(msip[i]);
        if (msip[i]=="1") {
            resultip+="0";
        }else{
            resultip+=ipstr[i];
        }
    }
    if (parseInt(resultip)==0) {
        return true;
    }
}
function get_ip6_reg (mask) {
    var regStr = "^((([0-9A-Fa-f]{1,4}:){6}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:)))(%.+)?";
    var maskStr = "(/([0][0-9]{1,2}|[0-9]{1,2}|1[0-1][0-9]|12[0-8]))";
    if (typeof mask == "undefined" || mask != false) {//非无掩码
        regStr += maskStr;//有掩码
         if (typeof mask == "undefined") {//可有可无掩码
             regStr += "?";
        }
    }
    regStr += "$";
    var reg = new RegExp(regStr);
    return reg;
}
function validate_ip6(name, mask){
    var re = get_ip6_reg(mask);
    var item = validate_trim(document.getElementsByName(name)[0].value);
    if (re.test(item)) {
        return true;
    }
    return false;
}

function validate_ip6_nomask(name){
	var re = get_ip6_reg(false);
	var item = validate_trim(document.getElementsByName(name)[0].value);
	if (re.test(item)) {
		return true;
	}
	return false;
}

function validate_port(name, msg) {
	var reg=/^([0-9])([\w]*)$/;
	var str = document.getElementsByName(name)[0].value;
	 if(str*1>=0&&str*1<65536&&reg.test(str)){
		return true;
	}
	alert(msg);
	return false;
}

function validate_mac(name, msg) {
	var re = /^([0-9A-F]{2}[-:]){5}[0-9A-F]{2}$/i;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	alert(msg);
	return false;
}

function validate_mac_interface(name){
	var re = /^([0-9A-F][02468ACE][-]([0-9A-F]{2}[-]){4}[0-9A-F]{2})|([0-9A-F][02468ACE][:]([0-9A-F]{2}[:]){4}[0-9A-F]{2})$/i;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	return false;
}

function validate_number(name, msg) {
	var re = /^[0-9]+$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	alert(msg);
	return false;
}

function validate_byte(name, msg) {
	var re = /^[0-9]+$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item) && item * 1 >= 0 && item * 1 < 256) {
		return true;
	}
	alert(msg);
	return false;
}

function validate_port(name, msg) {
	var re = /^[0-9]+$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item) && item * 1 >= 0 && item * 1 < 65536) {
		return true;
	}
	alert(msg);
	return false;
}


function validate_trim(str){  
	return str.replace(/(^\s*)|(\s*$)/g, "");
}

function validate_split(str){  
	str = str.replace(/(^\s*)|(\s*$)/g, "").replace(/\s/g," ");
	return str.split(" ");
}

function validate_comment_text(name,msg_value,msg_len){
	var reg = /&|>|<|\"|'/;
	var value = document.getElementsByName(name)[0].value;
	if(reg.test(value)){
		alert(msg_value);
		return false;
	}
	if(value.length<0 || value.length>255){
		alert(msg_len);
		return false;
	}
	return true;
}

//检查数据库下备注危险字符
function validate_comment_text_db(name,msg_value,msg_len){
	var reg = /^[ a-zA-Z0-9\u0391-\uFFE5\(\)\-_\{\}:\.,]*$/;
	var value = document.getElementsByName(name)[0].value;
    if(value.length<0 || value.length>255){
        alert(msg_len);
        return false;
    }
    if(reg.test(value)){
        return true;
	} else {
        alert(msg_value);
        return false;
	}
}

function validate_textlen(name,msg,len){
	len = len?len:256;
	var item = document.getElementsByName(name)[0].value;
	if(item.length <= len){
		return true;
	}
	alert(msg);
	return false;
}

function compareIP4(ipBegin, ipEnd)
{
    var temp1;
    var temp2;
    temp1 = ipBegin.split(".");
    temp2 = ipEnd.split(".");
    for (var i = 0; i < 4; i++)
    {
        var value1 = parseInt(temp1[i], 10);
        var value2 = parseInt(temp2[i], 10);
         if (value1>value2) {
            return 1;
        } else if (value1<value2) {
            return -1;
        }
    }
    return 0;
}

function validate_number_and_limit(name,start,end){
	var re = /^[0-9]+$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
        if(item<start||item>end){
        	return false;
        }
		return true;
	}
	return false;	
}

function validate_ipv6_autotunnel(name){
	var re = /^(0:0:0:0:0:0|:):((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\/96$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	return false;
}

function validate_ipv6_6to4(name){
    var re = /^2002:[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}:(.*)\/64$/;
    var ipv6Re = get_ip6_reg(true);
    var item = validate_trim(document.getElementsByName(name)[0].value);
    var matchResult = item.match(re);//查看是否符合某种格式2002:16进制:16进制:.../64
    if (!matchResult || !matchResult[0] || !matchResult[1]) {
        return false;
    }
    if (!ipv6Re.test(item)) {//检查是否为ipv6格式
        return false;
    }
    if (matchResult[1].indexOf("::") >= 0) {//是否有缩写成::
        if (ipv6Re.test(matchResult[1]+"/64")) {
            return true;
        }
    } else {
        if (/^([0-9a-fA-F]{1,4}:){4}[0-9a-fA-F]{1,4}$/.test(matchResult[1])) {
            return true;
        }
    }
    return false;
}

function validate_ipv6_compatiable(name){
	var re = /^(0:0:0:0:0:0|:):((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\/96)?$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	return false;
}

function get_utf8length(str){
    var re = '';
    var l = 0;
    var a = str.split("");
    for(var i=0;i<a.length;i++) {
        if (a[i].charCodeAt(0)<299) {
            l++;
         } else {
            l+=3;
         }
    }
    return l;
}

function validate_network_address(name){
	var re = /^([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.([0-9]|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.0$/;
	var item = document.getElementsByName(name)[0].value;
	if (re.test(item)) {
		return true;
	}
	
	return false;
}
