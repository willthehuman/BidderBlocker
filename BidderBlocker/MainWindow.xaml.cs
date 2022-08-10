using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using eBay;
using eBay.Service.Call;
using eBay.Service.Core.Sdk;
using eBay.Service.Core.Soap;

namespace BidderBlocker
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        ApiContext apiContext;

        //Instantiate the call wrapper class
        GeteBayOfficialTimeCall apiCall;

        //Send the call to eBay and get the results
        DateTime officialTime;
        public MainWindow()
        {
            InitializeComponent();
            InitializeEbayApi();
        }
        
        private void InitializeEbayApi()
        {
            apiContext = GetApiContext();

            //Instantiate the call wrapper class
            apiCall = new GeteBayOfficialTimeCall(apiContext);

            //Send the call to eBay and get the results
           officialTime = apiCall.GeteBayOfficialTime();
        }
        
        private void login_Click(object sender, RoutedEventArgs e)
        {
            //use the ebay sdk to authenticate the user
        }

        // Instantiating and setting ApiContext
        ApiContext GetApiContext()
        {
            //apiContext is a singleton,
            if (apiContext != null)
            {
                return apiContext;
            }

            else
            {
                apiContext = new ApiContext();

                //supply Api Server Url
                apiContext.SoapApiServerUrl = "https://api.sandbox.ebay.com/wsapi";

                //Supply user token
                ApiCredential apiCredential = new ApiCredential();

                //Just a partial token is shown for display purposes
                apiCredential.eBayToken = "BgBBBB**BQBBBB**BBBBBB**XrJITB**nY+sHZ2PrBmdj6wVnY+sEZ2PrB2dj6wFk4HoBJSDpQ6dj6x9nY+seQ**+FkBBB**BBMBBB**...";
                apiContext.ApiCredential = apiCredential;

                //Specify site: here we use US site
                apiContext.Site = SiteCodeType.US;

                return apiContext;
            } // else

        } //GetApiContext
    }
}
